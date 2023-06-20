# Documentation

Two decisions are fundamental in this context: the generator and the host. For the generator, we will utilize [MkDocs](https://www.mkdocs.org/), as an alternative to Sphinx. As for the host, we opt for [readthedocs](https://readthedocs.org/) over GitHub Pages. 

We suggest using [mkdocs-gallery](https://smarie.github.io/mkdocs-gallery/generated/tutorials/plot_parse/#download_links) instead of .ipynb notebooks for tutorials or examples. This is because mkdocs-gallery is easier to review and control versions while still providing the convenience of being downloadable or runnable on Binder as a notebook. These files should reside under the root directory: `examples/` (not `docs/examples/`). However, you can still include `ipynb` files (after clearing the outputs), as they are simpler for contributors to write and pair well with interactive visualization libraries. You can explore both options further [here](https://docs.readthedocs.io/en/stable/guides/jupyter.html) on the readthedocs page.

Reasoning behind these choices:
- MkDocs supports Markdown out-of-the-box, which is a more straightforward option than ReST.
- readthedocs enables building documentation for PRs, which is highly beneficial.

## Code References

The [mkdocstrings](https://mkdocstrings.github.io/) plugin for MkDocs allows you to generate the documentation directly from your Python code's docstrings, given they comply with certain standards (refer to the [docstrings](04-docstrings.md) note). 

Follow the steps below for the standard procedure:

1. Add the `mkdocstrings` plugin by modifying the **mkdocs.yml** `plugins` list.
```yaml
plugins:                         
    - mkdocstrings
    # other plugins...
```

2. Create a **docs/reference.md** file.

3. Automatically generate documentation for a script in your repository by editing the **reference.md**
file as follows,
```markdown
packagename:::your_script.py
packagename:::your_other_script.py
...
```

4. Incorporate the **reference.md** into your documentation's navigation structure by updating the **mkdocs.yml**,
```yaml
nav:
    - Home: index.md
    - Tutorials: generated/gallery
    - Workflow: notes/00-workflow.md
    - Structure: notes/01-structure.md
    - Packaging: notes/02-packaging.md
    - Documentation: notes/03-documentation.md
    - Docstrings: notes/04-docstrings.md
    - Linters and Tests: notes/05-linters-and-tests.md
    - CI: notes/06-ci.md
    - Data: notes/07-data.md
    - Open Source: notes/08-open-source.md
    - Code References: reference.md
```
## Automatic Code Referencing

As your project grows in complexity, you might need to automate the code referencing process rather than manually 
adding new scripts references.

Here's the procedure:

1. Ensure your project follows the recommended folder structure.

2. Copy and paste the `docs/gen_ref_pages.py` into your project's `docs/` directory. The script will run each time
mkdocs builds the documentation and will automatically create a `reference/` directory.

3. Confirm that the following plugins are listed in your `mkdocs.yml` file:

```yaml
plugins:
    - search                           # keep the search plugin enabled
    - mkdocstrings                     # plugin for generating documentation from Python docstrings
    - gen-files:
        scripts:
            - docs/gen_ref_pages.py
```

4. Add the **Code Reference** page to your documentation by adding it to the *nav* of the *mkdocs.yml*.

    ```yaml
    nav:
      # other pages in your documentation
      - Code References: reference/ # Note the trailing slash! It is needed so that mkdocs-literate-nav knows 
                                    # it has to look for a SUMMARY.md file in that folder.
    ``` 
    
For a more comprehensive overview of the automatic referencing setup, refer to [this guide](https://mkdocstrings.github.io/recipes/).

**Note on literate navigation:**

With the "literate-nav" plugin in MkDocs, you can enhance your documentation site's navigation by defining the navigation structure in a separate Markdown file, typically named **SUMMARY.md**. This file essentially serves as a table of contents or a navigation index for your documentation. When the repository is configured with the automatic referencing procedure detailed above, **SUMMARY.md** is temporarily created at build time by the **docs/gen_ref_pages.py** script and is subsequently removed.

### Considerations on Code Referencing

To summarize, automating code referencing offers the following benefits:

1. **Automatic Generation:** There's no need for manual creation of links or copying of code snippets into your 
documentation. The documentation remains up-to-date with each build.

2. **Dynamic Documentation:** As your code and its associated docstrings are updated, the documentation is regenerated.
Changes in script name or code structure do not affect your documentation, which stays up-to-date.

3. **Consistent Formatting:** The code reference structure is determined by the **docs/gen_ref_pages.py** script, 
ensuring consistency.

However, there's a caveat to the automatic generation process: it makes the process of code referencing more 
challenging to customize. To customize the code references layout, you would need to modify the **gen_ref_pages.py** 
script. On the other hand, manual referencing provides the flexibility to easily customize the layout of specific 
modules by editing the references.md file or by creating a dedicated markdown file for each module and making 
customizations there.

