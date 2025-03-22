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

# Update the date
cd manuscript/markdown
TODAY=$(date --iso-8601)
sed -i 's/\(Last updated on:\) *[0-9-]\{10\}/\1 '"$TODAY"'/' titlepage.md
sed -i 's/\(Last updated on:\) *[0-9-]\{10\}/\1 '"$TODAY"'/' titlepage-ebook.md
cd ../..

# Use titlepage-ebook.md for a simple title page
cd manuscript/markdown
mv titlepage.md titlepage-html.md
cp titlepage-ebook.md titlepage.md
cd ../..

$MDBOOK_EPUB_BIN --standalone

# Restore
mv book-html.toml book.toml
cd manuscript/markdown
mv titlepage-html.md titlepage.md
cd ../..

mv ./book/*.epub ./

# The epub is generated with the title as file name, but use a non-accented file name for storage.
mv "Nibbāna - The Mind Stilled.epub" "$EPUB_FILE"

~/bin/epubcheck "./$EPUB_FILE"

mv "./$EPUB_FILE" "./manuscript/markdown/assets/docs"

echo "OK"
