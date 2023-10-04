# Data

When writing software packages, we often would like to include data or other binary files to use in examples or testing. However, git does not play nicely with binary files: you cannot `diff` them easily, and so git stores the entire file each time it changes, which can cause your `.git` repository to get very large very quickly. In fact, git will warn you if you try to add a file larger than 50MB and [GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) will block any files larger than 100MB.

So what should you do?

The following are some helpful rules of thumb:

- Do not include any data files larger than 1MB in size in a git repo.
- If you do have data files (under that threshold), favor text formats (`.json`, `.yml`) over binary ones (`.npy`, `.pkl`). For example, if you're storing a small number of parameter values for a model, you can save them as a dictionary in a `.json` file. However, in some cases (such as images), you'll have no choice but to use a binary file format.
- Data should live in a dedicated folder, such as `data/` under the root directory. Note that this folder will *not* be included when packaging a python project, by default (and thus will not be present when people install from `pip`). If the data files are example inputs, this is probably fine, but if they are parameter values required by a model, you may want them included. In this case, you can either move them inside your source directory or add the paths to the [`MANIFEST.in`](https://packaging.python.org/en/latest/guides/using-manifest-in/#using-manifest-in) file.
- Files larger than 1MB should be uploaded to an external service. These files should only really be necessary in tests, tutorials, or documentation, and can thus be downloaded when necessary. See [the OSF section below](#using-the-osf-to-store-larger-data-files) for how to do so.
- Files larger than 5GB cannot be uploaded to the OSF and probably don't belong in documentation or tests. They may still be useful for workshops or other in-person events. In that case, consult with SCC about how to host storage.

## Using the OSF to store larger data files

The [Open Science Framework](https://osf.io/) is an open platform for managing research projects operated by the [Center for Open Science](https://www.cos.io/). Among other things, they provide file storage of up to 50GB per public project (which is what we want, since we'll be downloading this for our software library and don't want to deal with authenication), with an individual file size cap of 5GB. They also automatically version all files and allow you to mint DOIs for projects, to get a persistent URL to a specific version, if necessary. See their [FAQs](https://help.osf.io/article/555-add-ons-storage-api-integration-faq-s) for more details.

!!! example
    
    See [the repository of plenoptic presentations](https://github.com/LabForComputationalVision/plenoptic_presentations#assets) for an example of how this strategy is used, both interactively for the user and in Github actions.

!!! example
    
    See [this example](../../generated/gallery/plot_osf/) to see how to do the following in a cross-platform way using Python.

To use the OSF as a storage provider, do the following:

- If you do not have an account, create one [on the OSF website](https://osf.io).
- Create a project for your library. I recommend having a single project per library, to have everything in one place.
- Make the project public. OSF projects are private by default, but we need the project to be public so we can download its files without requiring authentication.
- Prepare your files. I recommend grouping files into zip or tar archives based on how they will be used. For example, one archive containing all files required for the tests and another for those required for the documentation.
- Upload your files. You can do this through the OSF website or via the [osfclient](https://github.com/osfclient/osfclient), a python command-line tool.
- Click on your newly uploaded file and note the url. It will be formatted something like `https://osf.io/{KEY}`, where `{KEY}` is an alphanumeric string of length 5 (e.g., `spu5e`).

    !!! warning
    
        This file URL will be different from that of your overall project! Make sure you're on the right page!

- You can then download this file using curl, replacing `{KEY}` as appropriate. Note that `curl` might not be present on Windows machines.
    ```bash 
    curl -O -J -L https://osf.io/{KEY}/download
    ```

- You'll then need to extract and arrange your assets. If you used `tar` (rather than `zip`), you can use the following:
    ```bash
    tar xvf PATH
    ```
