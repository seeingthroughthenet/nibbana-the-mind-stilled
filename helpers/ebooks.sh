#!/usr/bin/env bash

set -e

# without a specific path, it will use the binary installed by cargo
MDBOOK_EPUB_BIN=~/lib/mdbook-gambhiro/mdbook-epub-gambhiro-0.4.41

EBOOK_NAME="Nibbana-The-Mind-Stilled"
EPUB_FILE="$EBOOK_NAME.epub"
MOBI_FILE="$EBOOK_NAME.mobi"

# Use book-epub.toml to provide options
mv book.toml book-html.toml
cp book-epub.toml book.toml

$MDBOOK_EPUB_BIN --standalone

# Restore
mv book-html.toml book.toml

cd book/
# Use a non-accented file name.
mv "Nibbāna - The Mind Stilled.epub" "$EPUB_FILE"
~/bin/epubcheck "./$EPUB_FILE"

# ~/lib/kindlegen/kindlegen "./$EPUB_FILE" -dont_append_source -c1 -verbose

echo "OK"
