import sys, os

def getFilePath(filename):
    pathname = os.path.dirname(sys.argv[0])
    return "%s/%s" % (pathname, filename)