# Encounter a Penguin

> **Archived:** This is the historical incubation repository for Encounter
> Penguin. Active development moved to the University of Antarctica, and
> `University-of-Antarctica-Web` is the sole active source of truth. Do not
> synchronize this repository with the University project; make all new
> Encounter Penguin changes there.

An ordinary photograph. A brief visit from Professor Adelie.

## Historical migration snapshot

This standalone repository is retired and preserved only as migration
provenance for commit `975a030`. Encounter Penguin's sole active source of
truth is now the University of Antarctica repository at
`experiences/encounter-penguin/`.

Do not develop or deploy from this repository. There is no synchronization path
to the University repository.

## Local development

Requires Python 3.10 or newer.

```bash
python3 app.py
```

Open <http://127.0.0.1:8000> and choose a photograph.

After a quiet pause, Professor Adelie peeks in from an edge, stays briefly with a save option, then retreats. The photograph is never uploaded or modified.

## Character asset

The public product includes only the owner-approved Professor Adelie cutout
at `assets/professor-adelie-owner-approved.png`. The supplied PNG is preserved
unchanged; the browser uses its transparent bounds for placement. Raw photographs
and the broader source archive remain private and are not required by the
production build.

## Test it

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_static.py
```

The production artifact is written to `dist/`. Only `index.html`, `styles.css`,
`app-ui.js`, `.nojekyll`, and the owner-approved runtime PNG are included.
