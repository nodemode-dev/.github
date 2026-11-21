import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import apps_table

def app(id, name, state="live", licence="Apache-2.0", summary="Does one job.", repo=None):
    return {
        "id": id,
        "public": True,
        "app": id,
        "repo": repo or id,
        "repository": f"nodemode-dev/{repo or id}",
        "site": id,
        "name": name,
        "kind": "x",
        "summary": summary,
        "licence": licence,
        "state": state,
        "launcher": id,
        "agents": {"mcp": True, "skills": ""},
        "release": None,
    }


FAMILY = {
    "format": "formai-family",
    "format_version": 1,
    "generated": "2026-01-01T00:00:00Z",
    "source": {"repository": "nodemode-dev/formcompiler", "registry_version": "1.0.0"},
    "content_sha256": "0" * 64,
    "apps": [
        app("formcut", "FormCut", licence="GPL-3.0-only", summary="Video editing: cut and export."),
        app("formtxt", "FormTxt", state="prelaunch", summary="Not out yet."),
        app("formmd", "Form.md", summary="Notes | docs [x](y) <b>"),
        app("../evil", "Evil"),
        app("formslide", "FormDeck", repo="formdeck"),
        {"id": "formsecret", "public": False},
        {"id": "formhidden", "public": False, "name": "FormHidden", "state": "live", "summary": "private", "licence": "Apache-2.0"},
    ],
}


def test_only_public_live_apps_with_safe_slugs_are_listed():
    rows = apps_table.table(FAMILY)
    assert "[FormCut](https://formai.studio/formcut/) | Video editing: cut and export |" in rows
    assert "FormTxt" not in rows
    assert "Evil" not in rows


def test_the_listing_rule_today_is_state_live():
    assert apps_table.LISTING_RULE is apps_table.rule_a_state_live
    assert apps_table.rule_b_state_live({"state": "live"}) and not apps_table.rule_b_state_live({"state": "public"})


def test_the_release_rule_needs_a_published_version_and_still_skips_private_apps(monkeypatch):
    released = {"version": "1.2.3", "tag": "v1.2.3"}
    family = {
        "apps": [
            {**app("formcut", "FormCut"), "release": released},
            {**app("formtxt", "FormTxt", state="prelaunch"), "release": released},
            {**app("formnew", "FormNew", state="prelaunch"), "release": None},
            {**app("formempty", "FormEmpty"), "release": {"version": ""}},
            {"id": "formsecret", "public": False, "state": "live", "release": released},
        ]
    }
    assert [a["id"] for a in apps_table.shown(family)] == ["formcut", "formempty"]
    monkeypatch.setattr(apps_table, "LISTING_RULE", apps_table.rule_c_has_release)
    assert [a["id"] for a in apps_table.shown(family)] == ["formcut", "formtxt"]


def test_nothing_about_a_private_app_is_written():
    out = apps_table.render(f"{apps_table.START}\n{apps_table.END}\n{apps_table.LICENCE_START}\n{apps_table.LICENCE_END}\n", FAMILY)
    for word in ("formsecret", "FormHidden", "formhidden", "private"):
        assert word not in out


def test_links_to_the_site_use_the_machine_id_not_the_repository_name():
    rows = apps_table.table(FAMILY)
    assert "[FormDeck](https://formai.studio/formslide/) |" in rows
    assert "formdeck" not in rows


def test_rows_are_sorted_by_name_whatever_the_order_of_the_spec():
    reordered = {**FAMILY, "apps": list(reversed(FAMILY["apps"]))}
    assert apps_table.table(reordered) == apps_table.table(FAMILY)
    names = [r.split("]")[0][3:] for r in apps_table.table(FAMILY).splitlines()[2:]]
    assert names == ["Form.md", "FormCut", "FormDeck"]


def test_summaries_cannot_break_the_table_or_inject_markup():
    rows = apps_table.table(FAMILY)
    line = next(r for r in rows.splitlines() if "Form.md" in r)
    assert line == "| [Form.md](https://formai.studio/formmd/) | Notes docs x(y) b |"


def test_replace_keeps_everything_outside_the_markers():
    readme = f"intro\n{apps_table.START}\nold\n{apps_table.END}\nafter\n"
    out = apps_table.replace(readme, "NEW")
    assert out == f"intro\n{apps_table.START}\nNEW\n{apps_table.END}\nafter\n"


def test_missing_markers_and_an_empty_spec_fail_loudly():
    with pytest.raises(ValueError):
        apps_table.replace("no markers", "x")
    with pytest.raises(ValueError):
        apps_table.table({"apps": []})
    with pytest.raises(ValueError):
        apps_table.table({"apps": [{"id": "formsecret", "public": False}]})


def test_the_real_readme_has_the_markers():
    text = apps_table.README.read_text(encoding="utf-8")
    assert text.count(apps_table.START) == 1 and text.count(apps_table.END) == 1


def test_licence_line_is_derived_from_the_licences_of_the_listed_apps():
    assert apps_table.licences(FAMILY) == "Every repository states its own licence. Most apps are Apache-2.0; FormCut is GPL-3.0-only."
    only = {"apps": [app("formmd", "Form.md")]}
    assert apps_table.licences(only) == "Every repository states its own licence. Every app is Apache-2.0."
    split = {"apps": [app("a", "A", licence="MIT"), app("b", "B", licence="GPL-3.0-only"), app("c", "C", licence="GPL-3.0-only"), app("d", "D", licence="MIT")]}
    assert apps_table.licences(split) == "Every repository states its own licence. B and C are GPL-3.0-only; A and D are MIT."
    assert apps_table.licences({"apps": []}) == "Every repository states its own licence."


def test_a_listed_app_without_a_licence_is_refused():
    broken = {"apps": [{**app("formcut", "FormCut"), "licence": ""}]}
    with pytest.raises(ValueError):
        apps_table.licences(broken)


def test_the_real_readme_has_the_licence_markers():
    text = apps_table.README.read_text(encoding="utf-8")
    assert text.count(apps_table.LICENCE_START) == 1 and text.count(apps_table.LICENCE_END) == 1


@pytest.fixture()
def checkout(tmp_path):
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / "profile").mkdir()
    shutil.copy(Path(apps_table.__file__), root / "scripts" / "apps_table.py")
    shutil.copy(apps_table.README, root / "profile" / "README.md")
    family = tmp_path / "family.json"
    family.write_text(json.dumps(FAMILY), encoding="utf-8")
    return root, family


def run(root, family, *extra):
    return subprocess.run(
        [sys.executable, "-I", str(root / "scripts" / "apps_table.py"), "--family", str(family), *extra],
        capture_output=True,
        text=True,
        cwd=root,
    )


def test_check_writes_nothing_names_the_file_and_exits_1_on_drift(checkout):
    root, family = checkout
    readme = root / "profile" / "README.md"
    before = readme.read_bytes()
    result = run(root, family, "--check")
    assert (result.returncode, result.stdout.strip()) == (1, "profile/README.md")
    assert readme.read_bytes() == before


def test_write_then_check_is_current_and_the_same_spec_gives_the_same_bytes(checkout):
    root, family = checkout
    readme = root / "profile" / "README.md"
    assert run(root, family).returncode == 0
    first = readme.read_bytes()
    assert run(root, family, "--check").returncode == 0
    assert run(root, family).returncode == 0
    assert readme.read_bytes() == first
    text = first.decode("utf-8")
    assert "FormCut" in text and "formsecret" not in text and "2026-01-01" not in text and "0" * 20 not in text


def test_a_bad_spec_is_an_error_not_drift(checkout):
    root, family = checkout
    family.write_text(json.dumps({"format": "other", "apps": []}), encoding="utf-8")
    assert run(root, family, "--check").returncode == 2
    assert run(root, root / "missing.json", "--check").returncode == 2
