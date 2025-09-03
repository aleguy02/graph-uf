## Credit to @ufosc/SwampScheduler for original code

import json
import time
from typing import TypedDict, Any, List

import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://one.uf.edu/apix/soc/schedule"
semesters = {
    # 2018
    "f18": "2188",
    # 2019
    "sp19": "2191",
    "sm19": "2195",
    "f19": "2198",
    # 2020
    "sp20": "2201",
    "sm20": "2205",
    "f20": "2208",
    # 2021
    "sp21": "2211",
    "sm21": "2215",
    "f21": "2218",
    # 2022
    "sp22": "2221",
    "sm22": "2225",
    "f22": "2228",
    # 2023
    "sp23": "2231",
    "sm23": "2235",
    "f23": "2238",
    # 2024
    "sp24": "2241",
    "sm24": "2245",
    "f24": "2248",
    # 2025
    "sp25": "2251",
    "sm25": "2255",
    "f25": "2258",
}


def _generate_soc_request_url(
    term: str, program: str, last_control_number: int = 0
) -> str:
    """
    @rtype: str
    @param term: a string that corresponds to the term ('2228' --> Fall 2022)
    @param program: which UF program (ie. on campus/online/innovation)
    @param last_control_number: effectively, the number of courses to skip before scraping
    @return: the URL for the SOC request
    """
    parameters = {
        "term": term,
        "category": program,
        "last-control-number": last_control_number,
    }

    parameters_str = "&".join([f"{k}={v}" for k, v in parameters.items()])

    return f"{BASE_URL}?{parameters_str}"


class SOCInfo(TypedDict):
    term: str
    program: str
    scraped_at: int


class SOC(TypedDict):
    info: SOCInfo
    courses: List[Any]


def fetch_soc(
    term: str,
    program: str,
    last_control_number: int = 0,
    num_results_per_request: int = 50,
) -> SOC:
    """
    Fetches UF's schedule of courses.
    @rtype: list
    @param term: a string that corresponds to the term ('2228' --> Fall 2022)
    @param program: which UF program (ie. on campus/online/innovation)
    @param last_control_number: effectively, the number of courses to skip before downloading
    @param num_results_per_request: must be between 1 and 50
    @return: a list of the courses and their relevant information (from UF API)
    """

    assert (
        last_control_number >= 0
    ), "Last control number must be at least 0, {last_control_number} was given."
    assert (
        1 <= num_results_per_request <= 50
    ), f"Number of results per request must be between 1 and 50, {num_results_per_request} was given."

    soc: SOC = {
        "info": {"term": term, "program": program, "scraped_at": int(time.time())},
        "courses": [],
    }
    last = None
    while last is None or last["RETRIEVEDROWS"] == num_results_per_request:
        # If retrieved less than asked for we have gotten the final page of results

        next_last_control_num = (
            last["LASTCONTROLNUMBER"] if (last is not None) else last_control_number
        )
        url = _generate_soc_request_url(
            term, program, last_control_number=next_last_control_num
        )
        print(url)

        request = requests.get(url)
        last = json.loads(request.text)[0]
        soc["courses"].extend(last["COURSES"])
    return soc


def _scrape_one(s: str, term: str) -> tuple[str, bool, str | None]:
    """Scrape a single semester and write its JSON file.
    Returns tuple of (semester_key, success_flag, error_message_or_None).
    """
    try:
        print(f"=== fetching SoC - {s} ===")
        soc_scraped = fetch_soc(term, "CWSP")
        fp = os.path.join(os.getcwd(), "src", "json", f"soc_scraped_{s}.json")

        print(f"=== writing to {fp} ===")
        soc_str = json.dumps(soc_scraped)
        with open(fp, "w") as f:
            f.write(soc_str)

        print(f"DONE - {s}")
        return (s, True, None)
    except Exception as e:
        msg = str(e)
        print(f"!! An exception occurred for {s}: {msg} !!")
        return (s, False, msg)


def main():
    WORKERS = 8
    items = list(semesters.items())
    results: list[tuple[str, bool, str | None]] = []
    start = time.time()
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        future_map = {ex.submit(_scrape_one, s, term): s for s, term in items}
        for fut in as_completed(future_map):
            results.append(fut.result())

    duration = time.time() - start
    ok = [r for r in results if r[1]]
    failed = [r for r in results if not r[1]]

    print("=== SUMMARY ===")
    print(
        f"Total semesters: {len(results)} | Success: {len(ok)} | Failed: {len(failed)} | Elapsed: {duration:.1f}s"
    )
    if failed:
        print("Failed semesters:")
        for s, _, err in failed:
            print(f"  - {s}: {err}")


if __name__ == "__main__":
    main()
