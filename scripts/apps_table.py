import argparse
import json
import re
import sys
from pathlib import Path

SITE = "https://formai.studio"
FORMAT = "formai-family"
FORMAT_VERSION = 1
START = "<!-- apps:start -->"
END = "<!-- apps:end -->"
LICENCE_START = "<!-- licences:start -->"
LICENCE_END = "<!-- licences:end -->"
SLUG = re.compile(r"^[a-z0-9][a-z0-9.-]{0,40}$")
README = Path(__file__).resolve().parent.parent / "profile" / "README.md"
README_NAME = "profile/README.md"


def cell(text: str) -> str:
    flat = re.sub(r"[<>\[\]`*_|\\]", "", str(text))
    return " ".join(flat.split()).rstrip(".")


def table(family: dict) -> str:
    rows = ["| App | What it does |", "| --- | --- |"]
    for app in shown(family):
        slug = str(app["id"])
        name = cell(app.get("name", slug))
        rows.append(f"| [{name}]({SITE}/{slug}/) | {cell(app.get('summary', ''))} |")
    if len(rows) == 2:
        raise ValueError("the family spec lists no public live apps")
    return "\n".join(rows)


def rule_a_state_live(app: dict) -> bool:
    return app.get("state") == "live"


def rule_b_state_live(app: dict) -> bool:
    return app.get("state") == "live"


def rule_c_has_release(app: dict) -> bool:
    release = app.get("release")
    return isinstance(release, dict) and bool(str(release.get("version") or "").strip())


LISTING_RULE = rule_a_state_live


def shown(family: dict) -> list[dict]:
    apps = [
        a
        for a in family["apps"]
        if a.get("public") is True and LISTING_RULE(a) and SLUG.match(str(a.get("id", "")))
    ]
    return sorted(apps, key=lambda a: (cell(a.get("name", a["id"])).casefold(), str(a["id"])))


def joined(names: list[str]) -> str:
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"


def licences(family: dict) -> str:
    groups: dict[str, list[str]] = {}
    for app in shown(family):
        licence = cell(app.get("licence", ""))
        if not licence:
            raise ValueError(f"{app['id']} has no licence in the family spec")
        groups.setdefault(licence, []).append(cell(app.get("name", app["id"])))
    line = "Every repository states its own licence."
    if not groups:
        return line
    if len(groups) == 1:
        return f"{line} Every app is {next(iter(groups))}."
    total = sum(len(v) for v in groups.values())
    main = max(sorted(groups), key=lambda k: len(groups[k]))
    parts = []
    if len(groups[main]) * 2 > total:
        parts.append(f"Most apps are {main}")
        del groups[main]
    for licence in sorted(groups):
        names = joined(sorted(groups[licence], key=str.casefold))
        parts.append(f"{names} {'is' if len(groups[licence]) == 1 else 'are'} {licence}")
    return f"{line} {'; '.join(parts)}."


def replace(readme: str, rows: str, start: str = START, end: str = END) -> str:
    head, found, rest = readme.partition(start)
    if not found or end not in rest:
        raise ValueError(f"README has no {start} ... {end} block")
    return f"{head}{start}\n{rows}\n{end}{rest.split(end, 1)[1]}"


def render(readme: str, family: dict) -> str:
    return replace(replace(readme, table(family)), licences(family), LICENCE_START, LICENCE_END)


def load_family(path: str) -> dict:
    family = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(family, dict) or family.get("format") != FORMAT or family.get("format_version") != FORMAT_VERSION:
        raise ValueError(f"{path} is not a {FORMAT} version {FORMAT_VERSION} file")
    apps = family.get("apps")
    if not isinstance(apps, list) or not all(isinstance(a, dict) and "id" in a for a in apps):
        raise ValueError(f"{path} has no usable apps list")
    return family


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write or check the apps table and licence line in profile/README.md from family.json.")
    parser.add_argument("--family", required=True, help="path to family.json")
    parser.add_argument("--check", action="store_true", help="write nothing; exit 1 naming the file when it differs")
    args = parser.parse_args(argv)
    try:
        family = load_family(args.family)
        readme = README.read_bytes().decode("utf-8")
        updated = render(readme, family)
    except (OSError, ValueError) as error:
        print(f"apps_table: {error}", file=sys.stderr)
        return 2
    if updated == readme:
        print("apps table is current")
        return 0
    if args.check:
        print(README_NAME)
        return 1
    README.write_bytes(updated.encode("utf-8"))
    print("apps table updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
