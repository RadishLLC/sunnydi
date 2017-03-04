#!/bin/sh

# get the build number from the git commit count
BUILD=$(git rev-list HEAD --count)

# get the branch
BRANCH=$(git branch | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/')

# get the major/minor version from the git tag, parse it and pass it along to gradle
VERSION=$(git describe --long --tags | sed -E 's/^v([0-9]*)\.([0-9]*)\.[0-9]*-([0-9]*)-(.*)$/\1.\2.\3.\4/')
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
if [ "$*" = "ci" ]; then
    /usr/bin/env python setup.py version --major $MAJOR --minor $MINOR --revision $BUILD
else
    /usr/bin/env python setup.py version --major $MAJOR --minor $MINOR --revision $BUILD --variant $HASH
fi

RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "Generate version succeeded"
else
    echo "Generate version failed"
    exit 1
fi

# build the wheelhouse if it doesn't already exist
if [ ! -d ".wheelhouse" ]; then

    /usr/bin/env pip install wheelhouse
    /usr/bin/env wheelhouse build

    RESULT=$?
    if [ $RESULT -eq 0 ]; then
        echo "Generate wheelhouse succeeded"
    else
        echo "Generate wheelhouse failed"
        exit 1
    fi
fi

# run tox for code checks
/usr/bin/env tox

RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "Code checks succeeded"
else
    echo "Code checks failed"
    exit 1
fi

# build the source distribution
/usr/bin/env python setup.py sdist

RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "Generate source distribution succeeded"
else
    echo "Generate source distribution failed"
    exit 1
fi

# build the wheel distribution
/usr/bin/env python setup.py bdist_wheel

RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "Generate wheel distribution succeeded"
else
    echo "Generate wheel distribution failed"
    exit 1
fi
