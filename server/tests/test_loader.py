from src.loader import _extract_codes


def mock(c):
    prereqs = []
    tgt = c["code"].strip().upper()
    for p in _extract_codes(c.get("prerequisites", "")):
        prereqs.append(p)

    return tgt, prereqs


def test_loader():
    c1 = {
        "code": "COP3503C",
        "prerequisites": "Prereq: COP 3502C and MAC 2311 both with minimum grades of C.",
    }
    assert mock(c1) == ("COP3503C", ["COP3502C", "MAC2311"])

    c2 = {"code": "EGS6949", "prerequisites": "Coreq: EGS 6940."}
    assert mock(c2) == ("EGS6949", [])

    c3 = {
        "code": "COT3100",
        "prerequisites": "Prereq: (MAC 2311 or MAC 3472) and (COP 3502C or equivalent), all with a minimum grades of C; Coreq: COP 3504 or COP 3503.",
    }
    assert mock(c3) == ("COT3100", ["MAC2311", "MAC3472", "COP3502C"])
