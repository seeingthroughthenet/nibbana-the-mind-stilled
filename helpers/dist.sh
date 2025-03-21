#!/bin/bash

DOT_GIT_DIR="../nibbana-the-mind-stilled_gh-pages-dot-git"

MDBOOK_BIN=~/lib/mdbook-gambhiro/mdbook-gambhiro-0.4.43

if [ ! -d "$DOT_GIT_DIR" -o ! -f "$DOT_GIT_DIR/config" ]; then
    echo "Create the HTML repo .git folder as $DOT_GIT_DIR."
    exit 2
fi

if [ -d gh-pages ]; then
    $MDBOOK_BIN clean
fi

$MDBOOK_BIN build

# Relative path is interpreted from symlink target location, i.e. in ./gh-pages
ln -s "../$DOT_GIT_DIR" ./gh-pages/.git
