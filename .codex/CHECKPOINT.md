# Development checkpoint

## Objective

Operate Encounter Penguin independently of the owner's Mac through GitHub-driven continuous deployment to a persistent HTTPS URL.

## State

- Durable product, autonomy, raw-input, resource, and no-image-generation rules are persisted in `AGENTS.md` and `DESIGN.md`.
- Cloud-native operation is persisted in `AGENTS.md` and `DESIGN.md`: `main` is the production branch, GitHub Actions is the validation/build/deployment path, and GitHub Pages is the static HTTPS runtime.
- The sole active flow remains: upload → untouched pause → eased peek → visit/save window → eased retreat → original photograph.
- The owner-authorized Public / Private boundary is persisted in `AGENTS.md` and `DESIGN.md`. The repository is Public; raw photographs, corpus notes, and broader source archives remain Private. Access never implies publication.
- The playable product uses the owner's authoritative supplied cutout unchanged at `assets/professor-adelie-owner-approved.png`. Its transparent bounds are cropped only at render time for sizing and placement. The previous automated derivative is no longer part of the current product.
- The public repository was rebuilt from the audited current tree as a clean history. Historical private fixtures, raw sources, local paths, and internal corpus material are not reachable from public refs.
- The character is rendered on a separate transparent canvas; the uploaded photograph remains on its own canvas.
- Save creates a new PNG from both canvases only while the visitor is fully present.
- Encounters cover right, left, and bottom edges from a randomized starting direction, cycling through all three before repeating. Peak placement is direction-aware: side entries reveal 84% of the character width, bottom entry reveals 88% of the character height, and left entry mirrors the supplied pose so Professor Adelie faces inward. Every peak clearly presents the cap, face, head, and upper body while retaining an edge crop. Top entry is excluded because the upright source would introduce the body before the head.
- Visual-quality diagnosis found no encoding loss or asset upscaling: the approved PNG is lossless and its 1866×2485 visible crop exceeds the rendered character size. The app caps display at the upload's raster width, requests high-quality canvas resampling, and pixel-aligns the held pose.
- Runtime dependency audit: `index.html`, `styles.css`, `app-ui.js`, and `assets/professor-adelie-owner-approved.png` are production files. `app.py` is a local-development server. Tests and private source material are development-only. No runtime secrets, environment variables, backend, database, local mounts, or cloud configuration are required.
- `scripts/build_static.py` creates a whitelist-only `dist/` artifact and `.github/workflows/deploy-pages.yml` tests, builds, and deploys `main` with official GitHub Pages actions.

## Validation

- The owner-approved public PNG is preserved byte-for-byte at 1980×3520 with SHA-256 `f566348a640dc2b735b962ffb3e950914e559f89e214fa8f395f40834a9ebafd`; its private raw source is not required by tests or the production build.
- JavaScript syntax, Python compilation, and deterministic static production builds pass.
- Visually inspected the owner-approved alpha asset and its runtime crop. The character's supplied pixels are unchanged; only transparent canvas margins are excluded during compositing.
- In-app browser QA passed at desktop and 390×844 mobile viewports with the sharper, reduced-scale visitor.
- Verified upload, untouched pause, eased entry, inward-facing placement, full visit/save state, downloadable PNG composition, retreat, disappearance, replay readiness, responsive layout, and zero console warnings/errors.
- Seven tests pass, including exact production-artifact membership and workflow assertions. The exact `dist/` build was served separately and passed the upload → encounter → save-state browser flow with zero console warnings/errors.
- The repository is public at `https://github.com/AssistantofProfDrAdelie/find_a_penguin` and GitHub Pages is configured for workflow deployment with HTTPS enforcement.
- GitHub Actions run `35116835940` completed successfully for direction-aware reveal commit `0ff2159`.
- The production site at `https://assistantofprofdradelie.github.io/find_a_penguin/` returns HTTPS 200 and serves the approved asset with the exact local SHA-256. Live-browser QA verified upload, encounter, visible save, successful PNG download, complete retreat, replay readiness, and zero console warnings/errors.

## Next action

Owner product evaluation of the live encounter. No engineering or publication blocker remains.
