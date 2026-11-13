import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import apps_table

CATALOGUE = {
    "products": [
        {"id": "formcut", "name": "FormCut", "state": "live", "licence": "GPL-3.0-only", "summary": "Video editing: cut and export."},
        {"id": "formtxt", "name": "FormTxt", "state": "soon", "summary": "Not out yet."},
        {"id": "formmd", "name": "Form.md", "state": "live", "summary": "Notes | docs [x](y) <b>"},
        {"id": "../evil", "name": "Evil", "state": "live", "summary": "bad slug"},
    ]
}


def test_only_live_apps_with_safe_slugs_are_listed():
    rows = apps_table.table(CATALOGUE)
    assert "[FormCut](https://formai.studio/formcut/) | Video editing: cut and export |" in rows
    assert "FormTxt" not in rows
    assert "Evil" not in rows


def test_summaries_cannot_break_the_table_or_inject_markup():
    rows = apps_table.table(CATALOGUE)
    line = next(r for r in rows.splitlines() if "Form.md" in r)
    assert line == "| [Form.md](https://formai.studio/formmd/) | Notes docs x(y) b |"


def test_replace_keeps_everything_outside_the_markers():
    readme = f"intro\n{apps_table.START}\nold\n{apps_table.END}\nafter\n"
    out = apps_table.replace(readme, "NEW")
    assert out == f"intro\n{apps_table.START}\nNEW\n{apps_table.END}\nafter\n"


def test_missing_markers_and_empty_catalogue_fail_loudly():
    with pytest.raises(ValueError):
        apps_table.replace("no markers", "x")
    with pytest.raises(ValueError):
        apps_table.table({"products": []})


def test_the_real_readme_has_the_markers():
    text = apps_table.README.read_text(encoding="utf-8")
    assert text.count(apps_table.START) == 1 and text.count(apps_table.END) == 1


def test_licence_line_names_the_live_gpl_apps():
    assert apps_table.licences(CATALOGUE) == "Every repository states its own licence. Most apps are Apache-2.0; FormCut is GPL-3.0-only."
    assert apps_table.licences({"products": []}) == "Every repository states its own licence. Most apps are Apache-2.0."


def test_the_real_readme_has_the_licence_markers():
    text = apps_table.README.read_text(encoding="utf-8")
    assert text.count(apps_table.LICENCE_START) == 1 and text.count(apps_table.LICENCE_END) == 1
