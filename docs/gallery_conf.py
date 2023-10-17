"""
MkDocs Gallery Configuration script.

Modified from https://github.com/smarie/mkdocs-gallery/blob/main/docs/gallery_conf.py
"""
import os
import re
import sys

from mkdocs_gallery.gen_gallery import DefaultResetArgv
from mkdocs_gallery.sorting import FileNameSortKey

min_reported_time = 0
if "SOURCE_DATE_EPOCH" in os.environ:
    min_reported_time = sys.maxint if sys.version_info[0] == 2 else sys.maxsize

# To be used as the "base" config,
# this script is referenced in the mkdocs.yaml under `conf_script` option: docs/gallery_conf.py
conf = {
    "reset_argv": DefaultResetArgv(),
    "min_reported_time": min_reported_time,  # report runtime if larger than this value
    "within_subsection_order": FileNameSortKey,  # order your section in file name alphabetical order
    "filename_pattern": re.escape(os.sep)
    + "run",  # sets the pattern of scripts that will be executed, in this case any script starting with "run"
}
