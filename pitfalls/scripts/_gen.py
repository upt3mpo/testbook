"""Authoring helper (not run by learners): writes the shared page shell for a pitfall edition."""
import pathlib

SHELL = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} - {edition}</title>
    <style>
      body {{ font: 16px/1.5 system-ui, sans-serif; margin: 2rem; color: #111; background: #fff; }}
      .edition {{ font-size: 0.875rem; color: #444; }}
      .card {{ max-width: 32rem; border: 1px solid #767676; border-radius: 8px; padding: 1rem; }}
      button, input {{ font: inherit; }}
      button {{ padding: 0.5rem 0.9rem; border: 1px solid #444; border-radius: 6px; background: #eee; color: #111; }}
      input {{ padding: 0.5rem; border: 1px solid #444; border-radius: 6px; width: 100%; box-sizing: border-box; }}
      button:focus-visible, input:focus-visible, [tabindex]:focus-visible {{ outline: 3px solid #1264d0; outline-offset: 2px; }}
{style}
    </style>
  </head>
  <body>
    <main>
      <p class="edition">Pitfall: {title} (<strong>{edition}</strong> edition)</p>
{body}
    </main>
{script}
  </body>
</html>
"""


def page(directory, edition, title, style="", body="", script=""):
    path = pathlib.Path(directory) / edition
    path.mkdir(parents=True, exist_ok=True)
    script_block = f"    <script>\n{script}\n    </script>" if script else ""
    (path / "index.html").write_text(
        SHELL.format(title=title, edition=edition, style=style, body=body, script=script_block),
        encoding="utf-8",
    )
