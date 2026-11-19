# HASHOUT_LOG · scripts · .github

Living log of all comment content, explainers, rationale, TODOs and removed code for the scripts and the workflow in this repository. The source files stay comment-free; everything they would have said lives here, indexed. Read this first, then edit code surgically.

Current build version: none (this repository has no version)
Last updated: 2026-11-19 · apps_table.py reads the family spec instead of the site's catalogue

### apps_table.py · the table and the licence line come from family.json, offline
- refers-to: scripts/apps_table.py :: main, load_family, shown, table, licences, render; .github/workflows/apps-table.yml
- kind: change
- logged: 2026-11-19

The owner decided that the public apps table and the licence sentence must come from the family spec that nodemode-dev/formadaptor builds (family.json, `format` `formai-family`, version 1), not from fetching the website's catalogue. The script follows formadaptor's generator contract (docs/TARGETS.md): `--family PATH` writes the two generated blocks of `profile/README.md`; `--check` writes nothing, prints `profile/README.md` and exits 1 when the committed file differs, exits 0 when it is current. Any other failure (an unreadable or wrong-format spec, a README without its markers, a listed app without a licence, no public live app at all) exits 2 and writes nothing, so drift and breakage can never be confused. There is no network call; the script is standard library only and runs as `python3 -I`.

Which apps show is the rule the table already had, mapped onto the spec: the entry has `public` true, `state` is `live`, and the machine id passes the slug pattern. An entry with `public` false is skipped before any other field is read, so nothing about it can reach the file. `generated` and `content_sha256` are never read.

Links go to `https://formai.studio/<id>/` with the machine id (`formslide` for FormDeck, `formai` for FormPortal), not the repository name (`formdeck`, `formportal`). The table has no repository links today; if one is added it must use `repo`.

Order: the old table followed the catalogue's hand-kept order, which the spec does not carry (it is sorted by id, which would put FormDeck between FormSkills and FormSurface). Rows are sorted by name, case-insensitively, then id, so the same spec always gives the same bytes and a reader finds an app alphabetically. A curated order would need a field in the spec.

Names and summaries are the registry's wording, passed through the same `cell` clean-up as before (no markup characters, no trailing full stop). That is why a few names and sentences differ from the committed file when the registry words them differently.

The licence sentence is derived from the licences of the apps the table lists. If one licence covers more than half of them the sentence says "Most apps are X" and names the apps of every other licence ("A and B are Y"); if no licence has a majority every licence is listed with its apps; if there is only one licence it says "Every app is X". The old rule only knew Apache-2.0 and "starts with GPL"; a new licence would have been silently called Apache-2.0.

The README is read and written as bytes so line endings are never changed.

The tests that fetched nothing but built a catalogue dictionary were rewritten for the spec's shape (`apps`, `public`) because the function arguments and the empty-list message changed. Added: private entries leave no trace, the site link uses the id, sort order, licence variants, and a subprocess run in a temporary copy of the checkout for `--check` (writes nothing, exit 1 naming the file, exit 0 after a write, exit 2 on a bad spec) and for determinism.
