# Systems, made visible

A dependency-free interactive experience built for the KAISER GitHub profile.

Open `index.html` in a modern browser. Pointer/touch gestures can move project nodes; domain filters and connection modes redraw the SVG, and a live inspector reveals public-source evidence. Keyboard: left/right arrows for projects, 0–4 for filters, ? for shortcuts and Esc to close.

This is the actual interactive counterpart of the profile's 40-frame generated GIF. No third-party runtime, ads, trackers, private code or remote project data are embedded.

## Validation

```bash
python tools/check_experience.py
python -m unittest discover -s tests -p 'test_experience.py'
```

The profile repository publishes this folder through the GitHub Pages workflow when Pages is enabled under the repository's Settings. The Astro portfolio also includes a copy at its `/explore/` route, subject to that site's existing manual publishing process.
