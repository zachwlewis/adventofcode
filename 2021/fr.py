"""This supports easy loading of files as text."""

import sys
import os

def get_file_path(filename: str) -> str:
    """Creates an absolute path from a filename."""

    pathname = os.path.dirname(sys.argv[0])
    return "%s/%s" % (pathname, filename)

def read_as_list(filename: str) -> list[str]:
    """Reads a file in as a list of strings."""
    raw_lines = open(get_file_path(filename), 'r').readlines()
    return list(map(lambda s: s.strip(), raw_lines))
