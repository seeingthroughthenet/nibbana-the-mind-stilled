#!/usr/bin/env bash

for i in ./manuscript/markdown/sermon-*.md; do
    echo `basename $i`
    name=$(basename $i .md)
    cat "$i" | \
        sed -e '/<div/,/<\/div>/d; /^# /d;' | \
        pandoc -f markdown -t markdown --wrap=none \
        > "./manuscript/markdown-nowrap/$name-nowrap.md"
done
