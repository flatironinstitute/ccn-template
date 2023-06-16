# Documentation

Two decisions need to be made: generator and host. We'll use [MkDocs](https://www.mkdocs.org/) (instead of sphinx) for generator and [readthedocs](https://readthedocs.org/) (instead of github pages) for host.

Prefer [mkdocs-gallery](https://smarie.github.io/mkdocs-gallery/generated/tutorials/plot_parse/#download_links) to .ipynb notebooks for examples/tutorials, because it's easier to version control and review, while still being downloadable / runnable on binder as a notebook. They should live under the root directory: `examples/` (not `docs/examples/`). However, `ipynb` files can still be included (though outputs should probably be cleared), because they're easier for contributors to write and work better with interactive visualization libraries -- look into both of these. See [this](https://docs.readthedocs.io/en/stable/guides/jupyter.html) readthedocs page.

Rationale:
- MkDocs supports markdown out-of-the-box, which is much better than ReST
- readthedocs supports building documentation for PRs, which is very helpful.

## Automatic code referencing

As your project gets more complex, you may need to automate the process of generating the code references. 

In order to automate code referencing, you may follow these steps:

1. Check that the project follows the [recommended folder structure](01-structure.md#package-structure).

2. Copy/paste the `docs/gen_ref_pages.py` in your project `docs/` folder. The script will be run each time mkdocs builds the documentation and will create automatically a `reference/` folder.

3. Make sure that the following plug-ins are listed in your `mkdocs.yml` file:

    ```yaml
    plugins:
        - search                           # make sure the search plugin is still enabled
        - mkdocstrings                     # plugin for generating documentation from Python docstrings
        - gen-files:
            scripts:
                - docs/gen_ref_pages.py     # script for generating reference pages
        - literate-nav:
              nav_file: docs/SUMMARY.md     # navigation file for literate navigation
        - section-index                    # plugin for creating section index
    ```

4. Add the **Code Reference** page to your documentation by adding it to the *nav* of the *mkdocs.yml*.

    ```yaml
    nav:
      # other pages in your documentation
      - Code References: reference/ # Note the trailing slash! It is needed so that mkdocs-literate-nav knows 
                                    # it has to look for a SUMMARY.md file in that folder.
    ``` 
    
For a more detailed description of the automatic referencing setup, see [here](https://mkdocstrings.github.io/recipes/).

**Note on literate navigation:**

In the context of MkDocs, the "literate-nav" plugin enhances the navigation capabilities of your documentation site by allowing you to define the site's navigation structure in a separate Markdown file (often named SUMMARY.md). This file acts as a table of contents or navigation index for your documentation.
