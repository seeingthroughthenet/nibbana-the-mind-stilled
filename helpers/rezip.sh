#!/usr/bin/env bash

EPUB_NAME="Nibbana - The Mind Stilled.epub"
build_dir="Nibbana - The Mind Stilled"

cd book/

if [[ -f "$EPUB_NAME" ]]; then
    rm "$EPUB_NAME"
fi

{ cd "$build_dir" \
  && zip -X0 "../$EPUB_NAME" mimetype \
  && zip -rg "../$EPUB_NAME" META-INF -x \*.DS_Store \
  && zip -rg "../$EPUB_NAME" OEBPS -x \*.DS_Store \
  && cd -; } > zip.log 2>&1
