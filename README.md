# Encounter a Penguin

An ordinary photograph. A brief visit from Professor Adelie.

## Live application

The production application is deployed from `main` to GitHub Pages:

<https://assistantofprofdradelie.github.io/find_a_penguin/>

Pushes to `main` run tests, build a minimal static artifact, and deploy it. The
deployed application is browser-only: it needs no server, secrets, database, or
access to the owner's computer or raw asset archive.

## Local development

Requires Python 3.10 or newer.

```bash
python3 app.py
```

Open <http://127.0.0.1:8000>, choose a photograph, and press **Encounter a Penguin**.

Professor Adelie pauses, peeks in from an edge, stays briefly with a save option, then retreats. The photograph is never uploaded or modified.

## Character asset

The public product includes only the approved processed Professor Adelie cutout
at `assets/professor-adelie-transparent.png`. Raw photographs and the broader
source archive remain private and are not required by the production build.

## Test it

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_static.py
```

The production artifact is written to `dist/`. Only `index.html`, `styles.css`,
`app-ui.js`, `.nojekyll`, and the cleaned runtime PNG are included.
