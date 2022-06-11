import glob, os
from shutil import copytree
from fnmatch import filter
fontDirs = list()


# copy this file to whatever directory needs to be searched, ie. C:/Users/initi/Downloads,
# and run, have to change newFontDir as well

def checkIfFontDir(files):
    count = 0
    for file in files:
        if file.endswith(".pes"):
            count += 1
    return count > 25

def include_patterns(*patterns):
    """Factory function that can be used with copytree() ignore parameter.

    Arguments define a sequence of glob-style patterns
    that are used to specify what files to NOT ignore.
    Creates and returns a function that determines this for each directory
    in the file hierarchy rooted at the source directory when used with
    shutil.copytree().
    """
    def _ignore_patterns(path, names):
        keep = set()
        for pattern in patterns:
            keep.update(filter(names, pattern))
        ignore = set()
        for name in names:
            if name not in keep and not os.path.isdir(os.path.join(path, name)):
                ignore.add(name)
        return ignore
    return _ignore_patterns


for root, dirs, files in os.walk("."):
    if checkIfFontDir(files):
        fontDirs.append(root)

for fontDir in fontDirs:
    newFontDir = "C:/Users/initi/Fonts/" + fontDir[2:]
    copytree(fontDir, newFontDir, ignore=include_patterns('*.pes'))
