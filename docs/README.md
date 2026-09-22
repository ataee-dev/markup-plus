# Markup+ Documentation

Official documentation website for Markup+.

**Live:** https://ataee-dev.github.io/markup-plus/

## Structure

    docs/
    ├── index.html              Home page
    ├── examples/               18 interactive examples
    ├── guides/                 In-depth guides
    ├── api/                    API reference
    ├── playground/             Online editor
    ├── assets/                 CSS, JS, images
    └── mup-sources/            Source .mup files

## Local development

    cd docs
    python -m http.server 8000

Then open: http://localhost:8000

## Deployment

Automatically deployed via GitHub Pages from the `docs/` folder.

Settings → Pages → Source: `main` branch → `/docs` folder