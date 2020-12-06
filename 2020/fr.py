import sys, os, math
from typing import List

def getFilePath(filename: str) -> str:
  """Creates an absolute path from a filename."""

  pathname = os.path.dirname(sys.argv[0])
  return "%s/%s" % (pathname, filename)

def readAsList(filename: str) -> List[str]:
  rawLines = open(getFilePath(filename), 'r').readlines()
  return list(map(lambda s: s.strip(), rawLines))
