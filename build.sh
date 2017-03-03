#!/bin/sh

# get the build number from the git commit count
BUILD=$(git rev-list HEAD --count)

if [ -z "$BRANCH" ]; then
    # build branch
    BRANCH=$(git branch | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/')
fi

# get the major/minor version from the git tag, parse it and pass it along to gradle
VERSION=$(git describe --long | sed -E 's/^v([0-9]*)\.([0-9]*)-([0-9]*)-(.*)$/\1.\2.\3.\4/')
IFS='.' read -a versionparts <<< "$VERSION"

MAJOR=${versionparts[0]}
if [ -z "$MAJOR" ]; then
    MAJOR=0
fi

MINOR=${versionparts[1]}
if [ -z "$MINOR" ]; then
    MINOR=0
fi

OFFSET=${versionparts[2]}
if [ -z "$OFFSET" ]; then
    OFFSET=0
fi

HASH=${versionparts[3]}

if [ -z "$MAJOR" ]; then
    MAJOR=0
fi

#echo "Version: $VERSION"
#echo "Major: $MAJOR"
#echo "Minor: $MINOR"
#echo "Build: $BUILD"
#echo "Branch: $BRANCH"
#echo "Offset: $OFFSET"
#echo "Hash: $HASH"

# update the version from git branch info
if [ "$BRANCH" = "master" ]; then
    /usr/bin/env python setup.py version --major $MAJOR --minor $MINOR --revision $BUILD
else
    /usr/bin/env python setup.py version --major $MAJOR --minor $MINOR --revision $BUILD --variant $HASH
fi

# build the source distribution
/usr/bin/env python setup.py sdist

# build the wheel distribution
/usr/bin/env python setup.py bdist_wheel
