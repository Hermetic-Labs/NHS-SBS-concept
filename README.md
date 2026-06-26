# NHS SBS Healthcare AI Solutions — Intelligence Viewer

A lightweight, static intelligence viewer for the NHS SBS Healthcare AI Solutions framework (SBS10525). Browse clarification documents, Q&A databases, and media guides — all from a single page with zero backend required.

## Live Site

**[hermetic-labs.github.io/NHS-SBS-concept](https://hermetic-labs.github.io/NHS-SBS-concept/)**

## What's Here

| Path | Purpose |
|------|---------|
| `index.html` | The full single-page application (dark/light theme, document viewer, AI chat shell) |
| `data/cq_index.json` | Indexed clarification Q&A dataset for local keyword search |
| `data/markdown_docs/` | Framework literature rendered as browseable markdown |
| `data/images/` | Static assets (NHS logo) |

## Modes

### Simulator Mode (Static Hosting)
When served from GitHub Pages (or any static host), the viewer runs entirely client-side:
- **Document browsing** — Markdown docs rendered via `marked.js`
- **Q&A database** — Keyword search across the indexed clarification dataset
- **Media & guides** — Embedded video walkthroughs and webinar recordings

### Full Mode (Local Backend)
When paired with the local Python backend and desktop app, unlocks:
- **Deep AI semantic reasoning** powered by local LLM inference
- **Streaming chat responses** with context-aware document retrieval
- **Signed desktop installer** available via the download button

## Desktop App

The signed Windows desktop application bundles the full backend + AI engine. It is built locally with Tauri and signed via Azure Trusted Signing.

**Download:** Available through the chat interface on the live site, or directly from [Azure Blob Storage](https://hermeticlabs9f36.blob.core.windows.net/sbs-demo/desktop_app_0.1.0_x64-setup.exe).

> Desktop app source code is maintained locally and not tracked in this repository. This repo serves exclusively as the thin, public-facing static shell.

## Deployment

This site is deployed automatically via GitHub Actions on every push to `master`. See [`.github/workflows/pages.yml`](.github/workflows/pages.yml).

---

Built by [Hermetic Labs](https://hermeticlabs.com)
