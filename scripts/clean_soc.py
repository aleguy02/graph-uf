"""
Limit duplicate courses to their first instance
"""

import json, os
from scrape_soc import semesters

APP_DIR = "./"


def clean_soc(fp: str) -> dict:
    """
    Limits duplicate courses in UF's schedule of courses to their first instance
    @rtype: list
    @param fp: the file path of the source file being cleaned
    """
    courses = {}
    with open(fp, "r") as f:
        courses = json.load(f)
        courses = courses["courses"]

    course_names = set()
    res = []
    for course in courses:
        if course["name"] not in course_names:
            res.append(course)
            course_names.add(course["name"])

    return {"courses": res}


if __name__ == "__main__":
    for s, term in semesters.items():
        try:
            print(f"=== removing duplicates from SoC - {s} ===")
            fp = os.path.join(os.getcwd(), "src", "json", f"soc_scraped_{s}.json")
            without_duplicates = clean_soc(fp)

            fp = os.path.join(os.getcwd(), "src", "json", f"soc_cleaned_{s}.json")
            print(f"=== writing to {fp} ===")
            with open(fp, "w") as f:
                json.dump(without_duplicates, f)

            print("DONE")

        except Exception as e:
            print(f"!! An exception occured for {s}: {e} !!")
