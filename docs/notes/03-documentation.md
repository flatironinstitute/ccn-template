# Documentation

Two decisions need to be made: generator and host. We'll use [MkDocs](https://www.mkdocs.org/) (instead of sphinx) for generator and [readthedocs](https://readthedocs.org/) (instead of github pages) for host.

Use [mkdocs-gallery](https://smarie.github.io/mkdocs-gallery/generated/tutorials/plot_parse/#download_links) instead of .ipynb notebooks for examples/tutorials, because it's easier to version control and review, while still being downloadable / runnable on binder as a notebook. They should live under the root directory: `examples/` (not `docs/examples/`).

Rationale:
- MkDocs supports markdown out-of-the-box, which is much better than ReST
- readthedocs supports building documentation for PRs, which is very helpful.
