# A public observatory connected to the research archive

> **2026-09-18 amendment:** the identity and terminology in this original decision are superseded by [Author-defined identity and method](002-author-defined-method.md). P1 is oscillation, P2 self-reference and P3 coupling. The equation is immutable; reference documents have revisions. The static-site architecture remains in force.

## Decision

Build the TRIAD public experience as a small static site in `web/`, generated from the existing experiment catalog by `tools/build_site.py`. Publish through GitHub Pages. Keep English and Portuguese in one interface, with URL-addressable language and atlas filters.

The entrance presents the author's ontological hypothesis and nonstandard quantum-physics framing. It connects readers to original records, the complete equation, and its edition history. The visual field explorer reads saved density arrays; it does not execute or approximate the evolution equation. Comparing slices uses relative grid position and separately labeled density ranges.

## Why

The lab serves curious readers and people inspecting implementations. Its 65 studies already have a catalog and stable provenance. A static view can provide search, visual discovery and direct inspection without creating a second research database, accounts, a runtime service or duplicated scientific implementations.

## Delivery contract

- Every catalog study is discoverable in both maintained languages.
- Search, area and material filters combine and can be shared through the URL.
- Source images retain their original bytes. Original simulations, configurations and results remain untouched.
- The 1.1 equation reference is an additional, byte-exact edition; 1.0 remains available as historical context.
- Saved-state density inspection supports both datasets, axis selection, relative slice position and display scale. Each view links its source and identifies its range.
- Keyboard access, loading/failure/empty states and layouts at 320–1440 px are verified in the browser. The stylesheet respects reduced-motion preferences.
- Build output is generated, ignored by Git and published only after integrity checks and tests.

## Boundaries

The author's hypothesis is presented as such. The interface does not manufacture a definition for P1 or a conserved quantity for P1 + P2 + P3. No historical run is retroactively described as following reference 1.1. No numerical solver is altered or rerun by this work.
