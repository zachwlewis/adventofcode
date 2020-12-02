import sys, os, math

def getFilePath(filename: str) -> str:
  """Creates an absolute path from a filename."""

  pathname = os.path.dirname(sys.argv[0])
  return "%s/%s" % (pathname, filename)

def readAsList(filename: str):
  return open(getFilePath(filename), 'r').readlines()
