"""
Routes to serve main static pages. Not sure if this is how we'll do the frontend so we'll probably have to change it
"""

from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    current_app,
    request,
    abort,
)
from app.config import get_config

main_bp: Blueprint = Blueprint("main", __name__)
config = get_config()

import re

CODE_RE = re.compile(r"^[A-Z]{3,4}\d{4}[A-Z]?")


def normalise(code: str) -> str | None:
    m = CODE_RE.match(code.upper().replace(" ", ""))
    return m.group(0) if m else None


def _to_CSV(vals: list[str]) -> str | None:
    if not vals:
        return None
    return ",".join(vals)

def _resolve_selected_semesters(selected: str) -> tuple[str, list[str]]:
    """
    Returns (lookup_key, term_list).
    -if `selected` is an academic year key (like 'AY2025-2026'), the term list comes from app.config['AY_TERMS'][selected].
    -if list, split it
    -otherwise it is single term.
    """
    ay_terms = current_app.config.get("AY_TERMS", {})
    if selected in ay_terms:
        return selected, ay_terms[selected]
    if "," in selected:
        parts = [p.strip() for p in selected.split(",") if p.strip()]
        return selected, parts
    return selected, [selected]

@main_bp.route("/")
def index():
    """
    Returns home page
    """
    return render_template(
        "index.html",
        title="GraphUF",
        semesters=current_app.config["SEMESTERS"],
        default_semester=current_app.config["DEFAULT_SEMESTER"],
        academic_years=current_app.config.get("ACADEMIC_YEARS", current_app.config.get("AY_TERMS", {}).keys()),
        default_ay=current_app.config.get("DEFAULT_AY", current_app.config["DEFAULT_SEMESTER"]),
        max_courses_taken=config.MAX_COURSES_TAKEN,
    )
@main_bp.route("/unlocks", methods=["POST"])
def unlocks_redirect():
    raw = request.form.get("tentative-code", "")
    code = normalise(raw)
    if not code:
        return redirect(url_for("main.index"))

    # extract completed courses
    completed = []
    for i in range(1, config.MAX_COURSES_TAKEN + 1):
        raw = request.form.get(f"code{i}", "")
        if not raw:
            continue

        base = normalise(raw)
        if not base:
            return redirect(url_for("main.index"))

        completed.append(base)

    sem = request.form.get("semester", current_app.config["DEFAULT_SEMESTER"])

    view = request.form.get("view_type", "")
    if view != "tcm" and view != "graph":
        abort(400, "Bad view type")

    return redirect(
        url_for(
            "main.unlocks_page",
            code=code,
            completed=_to_CSV(completed),
            semester=sem,
            view_type=view,
        )
    )


@main_bp.route("/unlocks/<code>")
def unlocks_page(code: str):
    base = normalise(code)
    if not base:
        abort(400, f"Bad course code: {code}")

    completed_raw = request.args.get("completed", "")
    completed = set(completed_raw.split(",")) if completed_raw else set()

    # selected value may be AY key (like 'AY2025-2026'), comma list, or single term
    selected = request.args.get("semester", current_app.config.get("DEFAULT_AY", current_app.config["DEFAULT_SEMESTER"]))
    view = request.args.get("view_type", "")
    if view not in ("tcm", "graph"):
        abort(400, "Bad view type")

    # resolve to (lookup_key, terms)
    ay_key, term_list = _resolve_selected_semesters(selected)

    sem_set = set(term_list)

    struct = current_app.config["COURSE_TCM"] if view == "tcm" else current_app.config["COURSE_GRAPH"]

    try:
        if view == "tcm":
            unlocked = struct.postreqs(base, ay_key)
        else:
            #bfs over the union of requested terms
            unlocked = struct.postreqs(base, term_list)
    except ValueError:
        abort(400, f"Course not found in catalog: {base}")

    meet_prereqs = set()
    not_meet_prereqs = set()

    for c in unlocked:
        """
        compute direct prereqs for c under the union of selected terms.
        """
        graph = current_app.config["COURSE_GRAPH"]
        try:
            adj = graph.getAdjList()
            c_prereqs = {
                src
                for src, targets in adj.items()
                if c in targets and (targets[c] & sem_set)
            }
            if not c_prereqs.isdisjoint(completed) or c_prereqs == {base}:
                meet_prereqs.add(c)
            else:
                not_meet_prereqs.add(c)
        except (AttributeError, KeyError):
            abort(400, f"Course not found in catalog: {c}")
    # Build a merged tooltip map across the selected terms.
    # Prefer later terms first (e.g., sp26 over f25 over sm25).
    tooltip_union = {}
    for sem_code in reversed(term_list):  # latest first
        info = current_app.config["TOOLTIP_INFO"].get(sem_code, {})
        # only set if missing so later-term info wins
        for k, meta in info.items():
            tooltip_union.setdefault(k, meta)

    return render_template(
        "unlocks.html",
        title=f"{base} unlocks",
        code=base,
        not_meet_prereqs=sorted(not_meet_prereqs),
        meet_prereqs=sorted(meet_prereqs),

        # keep terms for legacy fallback in the templates
        semesters=current_app.config["SEMESTERS"],

        # academic-year dropdown (e.g., ["AY2025-2026", ...])
        academic_years=list(
            current_app.config.get("ACADEMIC_YEARS", current_app.config.get("AY_TERMS", {}).keys())
        ),

        # what the user picked (AY key like "AY2025-2026")
        selected_semester=ay_key,

        # single effective term for SOC links & tooltips (e.g., last term in the AY)
        effective_term=term_list[-1] if term_list else selected,

        # tooltip data keyed by the effective term
        tooltip_info=tooltip_union,

        # preserve selected data-structure toggle in the template
        view_type=view,
    )


