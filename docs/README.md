# Documentation

This repository uses **Sphinx/antsibull-docs** for documentation, not Jekyll.

## Documentation Location

The actual documentation for the Graphiant Playbooks Ansible Collection is located at:

```
ansible_collections/graphiant/naas/docs/
```

## Building Documentation

To build the documentation site, use the build script:

```bash
# From repository root
python scripts/build_docsite.sh
```

Or from the collection directory:

```bash
cd ansible_collections/graphiant/naas
./docs/build.sh
```

## Publishing

For GitHub Pages, the documentation should be published to a `gh-pages` branch, not from this `docs` folder.

See `ansible_collections/graphiant/naas/docs/DOCSITE_SETUP.md` for detailed instructions.

## GitHub Pages Configuration

If GitHub Pages is enabled, it should be configured to use the `gh-pages` branch, not the `/docs` folder.

To configure:
1. Go to repository Settings → Pages
2. Set Source to `gh-pages` branch (not `/docs` folder)
3. Or disable GitHub Pages if not using it
