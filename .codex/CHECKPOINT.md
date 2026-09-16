# Development checkpoint

## Objective

Operate Encounter Penguin independently of the owner's Mac through GitHub-driven continuous deployment to a persistent HTTPS URL.

## State

- Durable product, autonomy, raw-input, resource, and no-image-generation rules are persisted in `AGENTS.md` and `DESIGN.md`.
- Cloud-native operation is persisted in `AGENTS.md` and `DESIGN.md`: `main` is the production branch, GitHub Actions is the validation/build/deployment path, and GitHub Pages is the static HTTPS runtime.
- The sole active flow remains: upload → untouched pause → eased peek → visit/save window → eased retreat → original photograph.
- The owner-authorized Public / Private boundary is persisted in `AGENTS.md` and `DESIGN.md`. The repository is Public; raw photographs, corpus notes, and broader source archives remain Private. Access never implies publication.
- The playable product uses only the approved processed asset at `assets/professor-adelie-transparent.png`. Its raw photographic source and internal corpus notes are excluded from the current tree and are being purged from reachable Git history before publication.
- The invented SVG placeholder and its fixture are removed from the active tree. Git history preserves them.
- The character is rendered on a separate transparent canvas; the uploaded photograph remains on its own canvas.
- Save creates a new PNG from both canvases only while the visitor is fully present.
- Encounters alternate right and left edges; Professor Adelie's real left-facing pose is used on the right and mirrored only on the left so he always faces into the photograph.
- Runtime dependency audit: `index.html`, `styles.css`, `app-ui.js`, and `assets/professor-adelie-transparent.png` are production files. `app.py` is a local-development server. Asset preparation, OpenCV/Pillow/NumPy, tests, and private source material are development-only. No runtime secrets, environment variables, backend, database, local mounts, or cloud configuration are required.
- `scripts/build_static.py` creates a whitelist-only `dist/` artifact and `.github/workflows/deploy-pages.yml` tests, builds, and deploys `main` with official GitHub Pages actions.

## Validation

- The processed public PNG is served with the expected content; its private raw source is not required by tests or the production build.
- JavaScript syntax, Python compilation, and deterministic static production builds pass.
- Visually inspected the alpha at source scale and on a high-contrast background; no visible source-background halo remains around the cap, face, or tassel at product scale. The intentional lower crop is hidden beyond the photograph edge.
- In-app browser QA passed at the default desktop viewport and 390×844 mobile viewport.
- Verified upload, untouched pause, eased entry, inward-facing placement, full visit/save state, downloadable PNG composition, retreat, disappearance, replay readiness, responsive layout, and zero console warnings/errors.
- Seven tests pass, including exact production-artifact membership and workflow assertions. The exact `dist/` build was served separately and passed the upload → encounter → save-state browser flow with zero console warnings/errors.

## Next action

Complete the history purge and repeat the publication-safety audit. Then use the owner's explicit authorization to make the repository public, initialize Pages with `build_type: workflow`, rerun deployment, and verify the live HTTPS interaction.
