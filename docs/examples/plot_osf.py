#!/usr/bin/env python3
"""Downloading data from the OSF
=============================

This demonstrates how to use some small python functions to download files from
the OSF. We recommend storing binary files, especially those only needed for
testing and documentation, on the OSF and downloading them as needed. See the
[Data note](../../../notes/07-data) for more details about why you might want
to do this and how to get started.

After creating your OSF project and uploading your files, it's time to download
and extract them.

For this example, we're going to use a tarball from
[`plenoptic`](https://github.com/LabForComputationalVision/plenoptic/) which
contains some images used in the documentation.

!!! info

    A [tarball](https://en.wikipedia.org/wiki/Tar_(computing)) is an archive
    file created by the `tar` software utility, typically ending in `.tar` or
    `.tar.gz`, depending on whether it's been compressed. `.zip` is another
    common archive format.

First, we need to find the file's URL. In your browser, navigate to the
[plenoptic-files](https://osf.io/ts37w/) project and click on
`ssim_images.tar.gz` in the list under OSF Storage. This brings you to [this
page](https://osf.io/j65tw) which shows a minimal amount of metadata and an
explanation that OSF cannot view a tarball (understandably!). If we investigate
the url, we see that it is of the form `https://osf.io/{KEY}`, where `{KEY}` is
the string `j65tw`. Let's note that down, along with the generic OSF download
url.

"""

OSF_DOWNLOAD_URL = 'https://osf.io/{key}/download'
download_key = 'j65tw'

# %%
#
# We can download files in python using `requests`, which is included in the
# standard library. We also import `math` to do some calculations and the
# external library `tqdm`, which we use to get a nice error bar during download
# (this is unnecessary, but helpful, especially with larger files).

import requests
import math
from tqdm.auto import tqdm

def download_url(url: str,
                 destination_path: str = "./assets.tar.gz"):
    """Helper function to download `url` to `destination_path`
    """
    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)
    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024*1024
    wrote = 0
    with open(destination_path, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), unit='MB',
                         unit_scale=True,
                         total=math.ceil(total_size//block_size)):
            wrote += len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        raise Exception(f"Error downloading from {url}!")

# %%
#
# The above function will download any url, raising an exception if it looks
# like it failed based on the file size. It requires the URL to be correct and
# the project to be public, so double-check that!
#
# Let's download our file and look at its size.

import os
output_path = "./ssim_images.tar.gz"
download_url(OSF_DOWNLOAD_URL.format(key=download_key),
             output_path)
print(f'file size: {os.stat(output_path).st_size/1000}KB')

# %%
#
# Since our file is a tarball, we'll need to extract it, using the python
# standard library `tarfile`. Let's do that and investigate its contents.

import tarfile
def extract_tar(path: str = "./assets.tar.gz"):
    """Helper function to extract tarballs
    """
    with tarfile.open(path) as f:
        f.extractall(os.path.dirname(path))
    os.remove(path)


extract_tar(output_path)
output_dir = output_path.replace('.tar.gz', '')
file_list = "\n- ".join(os.listdir(output_dir))
print(f"Directory contents:\n- {file_list}")

# %%
#
# It can be also useful to programmatically check the date a file on the OSF
# has been modified (using the python standard library `json`), in order to see
# if we have recent local changes that we haven't uploaded yet. This isn't
# full-proof: it only checks the date modified, not the time, and you might be
# better off downloading the tarball and investigating the date modified of
# each individual file. But this can serve as a quick reminder to double-check
# if you have forgotten to upload anything new.

import json
def get_date_modified(file_url):
    """Gets date modified for OSF object
    """
    r = requests.get(f"{file_url}/metadata?format=datacite-json")
    meta = json.loads(r.text)
    mod = [d for d in meta['dates'] if d['dateType'] == 'Updated']
    if len(mod) != 1:
        raise Exception(f"Unable to find date modified for {file_url}!")
    return mod[0]['date']

# Note that we do NOT include the trailing `/download` found in
# `OSF_DOWNLOAD_URL` here.
file_url = f"https://osf.io/{download_key}"
remote_modified = get_date_modified(file_url)
print(f'OSF file date modified: {remote_modified}')

# %%
#
# And we can compare this against the modified time of our local file using
# `os` and `datetime`

from datetime import datetime
newest = 0
for f in os.listdir(output_dir):
    newest = max(newest, os.path.getmtime(os.path.join(output_dir, f)))
newest = datetime.fromtimestamp(newest)
print(f'Newest local object date modified: {newest.strftime("%Y-%m-%d")}')


# %%
#
# The output of `os.path.getmtime` is a [Unix
# timestamp](https://en.wikipedia.org/wiki/Unix_time), the number of seconds
# that have elapsed since midnight UTC on January 1, 1970. You can convert in
# and out of this format using python's `datetime` library, as above, and the
# timestamps are just floats and can be treated as such. For example, to find
# whether the remote or local object time is newer, we do the following.

remote_modified = datetime.strptime(remote_modified, "%Y-%m-%d")
time_diff = remote_modified.timestamp() - newest.timestamp()
if time_diff > 0:
    newer_file = 'Remote'
else:
    newer_file = 'Local'
print(f"{newer_file} file is {abs(time_diff)} seconds newer!")

# %%
#
# Note that we used the same format string to parse the remote file's timestamp
# as we used to convert the local timestamp for printing. See [the
# docs](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)
# for more details on allowed values here.
#
# Finally, if you have multiple files used by a single library, it might be
# helpful to maintain a dictionary linking the file names to the alphanumeric
# keys required in the url. The following is the library used in
# [plenoptic](https://github.com/LabForComputationalVision/plenoptic/):

OSF_URL = {'plenoptic-test-files.tar.gz': 'q9kn8',
           'ssim_images.tar.gz': 'j65tw',
           'ssim_analysis.mat': 'ndtc7',
           'msssim_images.tar.gz': '5fuba',
           'MAD_results.tar.gz': 'jwcsr',
           'portilla_simoncelli_matlab_test_vectors.tar.gz': 'qtn5y',
           'portilla_simoncelli_test_vectors.tar.gz': '8r2gq',
           'portilla_simoncelli_images.tar.gz':'eqr3t',
           'portilla_simoncelli_synthesize.npz': 'a7p9r',
           'portilla_simoncelli_synthesize_torch_v1.12.0.npz': 'gbv8e',
           'portilla_simoncelli_synthesize_gpu.npz': 'tn4y8',
           'portilla_simoncelli_scales.npz': 'xhwv3'}

# %%
#
# Then, to use the functions above, simply replace the `download_key` defined
# at the top of this file with `OSF_URL[filename]`.
#
# As the file extensions in the above dictionary show, you can upload other
# file types to the OSF as well! If your file is not a tarball, you can skip
# the extract step.
