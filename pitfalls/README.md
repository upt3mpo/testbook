# Pitfalls

Small, standalone pages that teach two skills Testbook alone cannot:

- **Catch it.** A page has a bug that slips past the obvious checks. Write the test that
  catches it.
- **Trust it?** A test is green. Decide whether you should believe it.

Each pitfall is a tiny page in plain HTML, CSS and JavaScript: no framework, no build step,
and the bug is visible in the source. They are deliberately **not** part of Testbook and
**not** part of its test suite. Testbook stays the clean product under test. Pitfalls are a
separate teaching bench with their own runner, their own dependencies and their own CI job.

Many are drawn from real Testbook bugs, and each README links to the real finding.

## Start here

```bash
cd pitfalls
npm install
npm run serve        # then open http://localhost:4100
```

Open a pitfall's **broken** page and use it by hand first. Then read its `README.md`, then try
its `exercise.md`.

## The shape of a pitfall

```text
catch-it/invisible-tab-stops/
  README.md          the story: what it is, why tests miss it, where it came from
  exercise.md        your task, with a hint ladder
  broken/index.html  the page with the bug
  fixed/index.html   the same page, corrected
  exercise/          YOUR starting files (JavaScript and Python)
  solution/          the reference tests (JavaScript and Python)
  suspect/           trust-it only: the green test you are asked to doubt
```

The `broken` and `fixed` pages differ in the smallest way that shows the lesson. The
`exercise/` and `solution/` folders each have a JavaScript file and a Python file, so both
tracks work through the same pitfall.

## How a pitfall proves itself

One test body runs against **both** pages. The runner expects it to fail on `broken` and pass
on `fixed`, and treats anything else as an error:

- If the reference test stops failing on the broken page, it no longer catches the bug, and
  the run reports an unexpected pass.
- If it fails on the fixed page, the fix (or the test) is wrong.

That is the same logic as mutation testing, applied to teaching material. It also means a
pitfall can never quietly stop teaching what it claims to teach.

To see the real failure instead of the expected one, run `npm run red -- <pitfall>`.

## Running things

| Command | What it does |
| --- | --- |
| `npm run serve` | Serve the pages on `http://localhost:4100` |
| `npm test` | Run every reference solution against both pages, plus the catalog checks |
| `npm test -- catch-it/silent-error` | One pitfall |
| `npm run exercise -- <pitfall>` | Run **your** test from `exercise/` against both pages |
| `npm run red -- <pitfall>` | Show the reference test actually failing on the broken page |
| `python3 -m pytest` | The Python reference solutions (install `requirements.txt` first) |
| `python3 -m pytest --exercises --show-red <pitfall>/exercise` | Your Python exercise |

The Python tests inject axe-core from `node_modules`, so run `npm install` once even if you
only follow the Python track.

## The pitfalls

| Shelf | Pitfall | Tests that miss it | What catches it |
| --- | --- | --- | --- |
| Catch it | Invisible Tab stops | axe, screenshots | Press Tab, watch focus |
| Catch it | The hover and click fight | axe | A real pointer plus `aria-expanded` |
| Catch it | A placeholder is not a label | axe | Find the field by its label |
| Catch it | The silent error | axe | The `alert` role, and where focus went |
| Catch it | A button inside a link | axe | Tab through the page and count the stops |
| Catch it | Lost focus | axe | Check where focus is after an action |
| Catch it | Every page has the same title | axe | The title and an announcement after navigating |
| Catch it | The theme nobody scanned | a default-theme scan | Reach the dark state, then scan it |
| Trust it? | The vacuous Escape test | the test itself | Assert the precondition first |
| Trust it? | The test id that hides the bug | functional tests using test ids | Find controls by role and name |

## Adding a pitfall

1. Pick a shelf and a slug: `catch-it/<slug>/` or `trust-it/<slug>/`.
2. Write `broken/index.html` and `fixed/index.html`. Keep the difference as small as you
   can. Everything except the one bug must stay correct (the catalog test checks the page
   has a language, title, `main` landmark and one `h1`).
3. Write the reference test once in JavaScript (`solution/`) and once in Python. Start the
   test body with `expectBugOnBroken(...)` / `expect_bug_on_broken(...)`.
4. If the lesson is "the usual tool is blind to this", add a test that proves the blindness
   (for example, a default axe scan passes on both pages).
5. For a trust-it pitfall, add the green-but-wrong test in `suspect/`.
6. Write `README.md` and `exercise.md` (with hints). Add a row to `index.html` and to the
   table above.
7. Run `npm test` and `python3 -m pytest`. `catalog.spec.js` fails if a piece is missing.

Prefer a real Testbook bug as the source, and link the audit finding. A bug a learner
recognises from a real app teaches more than an invented one.
