import json
import re
import sys
import urllib.request
from pathlib import Path

CATALOGUE = "https://formai.studio/catalog/v1/apps.json"
SITE = "https://formai.studio"
START = "<!-- apps:start -->"
END = "<!-- apps:end -->"
LICENCE_START = "<!-- licences:start -->"
LICENCE_END = "<!-- licences:end -->"
SLUG = re.compile(r"^[a-z0-9][a-z0-9.-]{0,40}$")
README = Path(__file__).resolve().parent.parent / "profile" / "README.md"


def cell(text: str) -> str:
    flat = re.sub(r"[<>\[\]`*_|\\]", "", str(text))
    return " ".join(flat.split()).rstrip(".")


def table(catalogue: dict) -> str:
    rows = ["| App | What it does |", "| --- | --- |"]
    for product in live(catalogue):
        slug = str(product["id"])
        name = cell(product.get("name", slug))
        rows.append(f"| [{name}]({SITE}/{slug}/) | {cell(product.get('summary', ''))} |")
    if len(rows) == 2:
        raise ValueError("the catalogue lists no live apps")
    return "\n".join(rows)


def live(catalogue: dict) -> list[dict]:
    return [p for p in catalogue.get("products", []) if p.get("state") == "live" and SLUG.match(str(p.get("id", "")))]


def joined(names: list[str]) -> str:
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"


def licences(catalogue: dict) -> str:
    gpl = [cell(p.get("name", p["id"])) for p in live(catalogue) if str(p.get("licence", "")).startswith("GPL")]
    line = "Every repository states its own licence. Most apps are Apache-2.0"
    return f"{line}; {joined(gpl)} {'is' if len(gpl) == 1 else 'are'} GPL-3.0-only." if gpl else f"{line}."


def replace(readme: str, rows: str, start: str = START, end: str = END) -> str:
    head, found, rest = readme.partition(start)
    if not found or end not in rest:
        raise ValueError(f"README has no {start} ... {end} block")
    return f"{head}{start}\n{rows}\n{end}{rest.split(end, 1)[1]}"


def fetch(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as answer:
        return json.load(answer)


def main() -> int:
    readme = README.read_text(encoding="utf-8")
    catalogue = fetch(CATALOGUE)
    updated = replace(replace(readme, table(catalogue)), licences(catalogue), LICENCE_START, LICENCE_END)
    if updated == readme:
        print("apps table is current")
        return 0
    README.write_text(updated, encoding="utf-8")
    print("apps table updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
