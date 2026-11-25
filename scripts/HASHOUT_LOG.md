# HASHOUT_LOG · scripts · .github

Living log of all comment content, explainers, rationale, TODOs and removed code for the scripts and the workflow in this repository. The source files stay comment-free; everything they would have said lives here, indexed. Read this first, then edit code surgically.

Current build version: none (this repository has no version)
Last updated: 2026-11-24 · the page lists the 29 apps the site shows as available, and the three of the 25 November launch (FormRig, FormCraft, FormPromo); 32 rows

### profile/README.md · three rows for the Group 6 launch of 25 November, written the day before
- refers-to: profile/README.md (between `apps:start` and `apps:end`, and the licence sentence)
- kind: change
- logged: 2026-11-24
- status: must not reach `main` before the launch, 25 November at noon Eastern (17:00 UTC)

The owner asked for an entry for the three apps that come out on 25 November. formcompiler's changelog for 0.22.0 names the Group 6 launch of that day: FormRig and FormCraft, registered then, and FormPromo, registered earlier. The site counts three apps for that date and does not name them yet.

- Order: after FormPublisher, at the end of the table, as FormRig, FormCraft, FormPromo. The site's own position for them could not be read before the launch; move the rows if the apps page places them elsewhere.
- Text: each app's `catalog.summary` in formcompiler's registry 0.22.0, without its last full stop.
- Links: `formai.studio/formrig/`, `/formcraft/` and `/formpromo/`, from each app's catalogue id. These pages do not answer before the launch, so the paths are not checked; every other app whose id and page path differ (FormPortal, FormDeck) is older.
- Licence sentence: FormPromo is GPL-3.0-only in the registry and is named last; FormRig and FormCraft are Apache-2.0. The three repositories are private today, so their LICENSE files were not read.

### profile/README.md · the table lists the 29 apps that are out, three rows added by hand
- refers-to: profile/README.md (between `apps:start` and `apps:end`, and the licence sentence); scripts/apps_table.py (not changed)
- kind: change
- logged: 2026-11-24

The owner asked for the page to carry the new releases. It listed 26 apps. The site's apps page shows 29 as available on 24 November: FormCAD, FormMorpheus and FormPublisher came out since the 21st (formcompiler registered FormMorpheus and FormPublisher in 0.21.0; its `releases.json` records formCAD v0.28.0 on the 23rd).

Their three rows were added by hand, as the nine of 21 November were and for the same reason, and the 26 existing rows were not touched.

- Order: the site's own product order. FormCAD after FormSculpt, FormMorpheus after FormFabric, FormPublisher after FormTools.
- Text: each app's one-line `catalog.summary` in formcompiler's registry (0.22.0, read on 24 November), without its last full stop. The family spec takes its summaries from there.
- Links: `formai.studio/formcad/`, `/formmorpheus/` and `/formpublisher/`, each read from the site's apps page on 24 November.
- Licence sentence: FormPublisher is GPL-3.0-only in the registry, so it joins the named apps, after Form.ext. FormCAD and FormMorpheus are Apache-2.0.

Still open, as before: `LISTING_RULE` and the generator. All three new apps are `prelaunch` in the registry, like most of the page.

### profile/README.md · the table lists the 26 apps that are out, nine rows added by hand
- refers-to: profile/README.md (between `apps:start` and `apps:end`); scripts/apps_table.py :: LISTING_RULE (not changed)
- kind: change
- logged: 2026-11-21

The owner asked for the page to be brought up to date. It listed 17 apps, the ones out by 10 November. The site's apps page shows 26 as available on 21 November: FormCel, FormTxt and FormTools (13 November), FormAT, FormRef and FormWeb (16 November), FormSurface, FormSculpt and FormFabric (19 November) came out since.

Their nine rows were added by hand and the 17 existing rows were not touched, because the generator would have rewritten those too: the family spec's names and one-line descriptions differ from the published ones (`formMCP`, `formskills`, `form.ext`, "Form app" where the page says "FormAI app"), it sorts by name where the page follows the site's order, and its ids for FormPortal and FormDeck (`formai`, `formslide`) are not the site's page paths (`formportal`, `formdeck`).

- Order: the site's own product order, which the 17 rows already followed. FormSurface and FormWeb after FormDeck; FormAT and FormCel after FormSkills; FormTxt and FormRef after FormPDF; FormSculpt, FormFabric and FormTools after Form.ext.
- Text: each app's one-line description from the family spec of 21 November, without its last full stop, as the other rows are written.
- Links: `formai.studio/[page]/`, each path read from the site's apps page on 21 November (`/format/` for FormAT).
- Licence sentence: unchanged. All nine are Apache-2.0 in the family spec.

Still open, as before: `LISTING_RULE` is `state == "live"`, which gives 11 rows from today's spec, so `--check` against the spec does not pass and the workflow does not run it. The rule that matches the page is "the site shows it as available", and the spec does not carry that.

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

### apps-table.yml · the workflow only checks; formadaptor opens the pull requests
- refers-to: .github/workflows/apps-table.yml :: check
- kind: change
- logged: 2026-11-19
- status: the `check` job and the network fetch described here were removed again on 2026-11-18, see "The page is not generated yet" below; the rest of this entry is the history of why the fetch was chosen and is superseded by the family decision to keep a copy of the spec in the target

The hourly job that fetched the site and opened `bot/apps-table-*` pull requests is gone. The workflow now runs the tests and then `apps_table.py --family <spec> --check` on pushes to main, on pull requests that touch the script, the tests, the README or the workflow, and by hand. There is no schedule: a scheduled check would turn red whenever the spec moves, which is exactly when formadaptor is about to open its own pull request. The `check` job needs no write permission (the workflow keeps `contents: read` only) and no token.

Where the spec comes from: docs/TARGETS.md lets a target either keep a copy of family.json or fetch it from formadaptor's `spec` branch. A committed copy would go stale, because formadaptor may change only the files declared for this target (`profile/README.md`), so its own pull request would fail a check against an older copy. The job therefore downloads https://raw.githubusercontent.com/nodemode-dev/formadaptor/spec/family.json with curl (retried, 60 second limit, fails on any HTTP error). The generator itself never touches the network. If formadaptor is private or the `spec` branch has not been published yet, the download fails with HTTP 404 and the job is red; that is a setup problem, not drift (the generator would have exited 2 or 1 by itself).

Action pins and Python 3.12 and pytest 8.3.3 are unchanged. Three bot pull requests (`bot/apps-table-*`) opened by the old job are still open on the live repository; the owner closes or merges them before this lands, because the new generator would rewrite the same blocks differently.

The tests that fetched nothing but built a catalogue dictionary were rewritten for the spec's shape (`apps`, `public`) because the function arguments and the empty-list message changed. Added: private entries leave no trace, the site link uses the id, sort order, licence variants, and a subprocess run in a temporary copy of the checkout for `--check` (writes nothing, exit 1 naming the file, exit 0 after a write, exit 2 on a bad spec) and for determinism.

### profile/README.md · the page is back to what was published until its source is settled
- refers-to: profile/README.md (apps and licences blocks)
- kind: revert
- logged: 2026-11-18

Regenerating from the family spec (commit e56835c) cut the table from 17 rows to 11 and shortened the licence line. The table lists only apps whose spec state is `live`; the spec, built from the registry, marks FormPortal and FormEncoder `public` and FormMCP, FormSkills, FormPDF and FormTray `prelaunch`, yet the page showed all six. Whether the registry states or the page is right is the owner's decision (it may mean changing the states in formcompiler's registry, or changing the rule here), so the page must not change until then. The file was restored to exactly the bytes of origin/main by two hand edits (the table block and the licence line); `git diff origin/main -- profile/README.md` prints nothing. The earlier commits are kept.

### apps-table.yml · The page is not generated yet, so the workflow only runs the tests
- refers-to: .github/workflows/apps-table.yml :: test
- kind: change
- logged: 2026-11-18

The `check` job is removed. With the page restored, `--check` against the sample spec would fail, and the job fetched the spec from a branch of formadaptor that does not exist yet. Family decision since: a target keeps a copy of the spec it was generated from in its own repository (here `scripts/family.spec.json`), the generator writes that copy only when its output changes, and CI checks against the copy with no network. This page is not generated from the spec until the owner settles the listing rule, so the workflow runs `pytest` on push to main and on pull requests (same paths), by hand too, and checks nothing else. Action pins, Python 3.12, pytest 8.3.3 and `contents: read` are unchanged. No spec copy is committed.

To switch on when the owner decides (in this order):
1. Pick the listing rule (next entry), delete the other two rules and the unused one's tests.
2. Run `python3 -I scripts/apps_table.py --family <family.json>` once. This is the first regeneration: it rewrites the apps and licence blocks of `profile/README.md`, and the generator must also write `scripts/family.spec.json` (the copy of the spec it was generated from) in the same run, only when its output changes. That copy-writing is not in the script yet and is part of this step.
3. Add to the workflow a `check` step after the tests: `python3 -I scripts/apps_table.py --family scripts/family.spec.json --check`. Local file, no network, no token.
4. Commit the regenerated README and the spec copy together, so the check is green from the first push.

### apps_table.py · the listing rule is one named line, with the three candidates the owner is choosing between
- refers-to: scripts/apps_table.py :: LISTING_RULE, rule_a_state_live, rule_b_state_live, rule_c_has_release, shown
- kind: change
- logged: 2026-11-18

`shown` keeps the entries with `public` true, a safe id and `LISTING_RULE(entry)` true. `LISTING_RULE` is one assignment, today `rule_a_state_live` (state is `live`, the rule the table already had), so behaviour is unchanged. Rule b is the same test as rule a, as the owner's brief lists it; it is a separate name only so that the choice can be written down, and if it was meant to differ it needs its definition. Rule c, `rule_c_has_release`, lists every public app that has a published release: `release` is an object with a non-empty `version`. The sample spec carries it: `release.version` (also `release.tag`, `release.published`, `release.url`, `release.skills`), present for every public app and `null` or absent for non-public ones. There is no command-line switch: the owner picks one rule, the other two go.

Under the sample spec (registry 0.16.0) the table shows 11 rows under a and b and 23 under c. Rule c brings back the six apps the page shows today (FormPortal, FormEncoder, FormMCP, FormSkills, FormPDF, FormTray) and also adds six the page has never shown, all `prelaunch` (Format, FormCel, FormRef, FormTools, FormTxt, FormWeb). Under c the licence line becomes "Most apps are Apache-2.0; form.ext, formMCP, FormPortal and formskills are GPL-3.0-only." The names formMCP, formskills and Format are the registry's own spelling.
