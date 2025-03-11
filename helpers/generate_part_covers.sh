#!/usr/bin/env bash

# associative array with keys, not index numbers
declare -A widths

widths[1]=944
widths[2]=946

for n in 1 2; do
    w=${widths[$n]}
    name=cover-$n

    cat cover-part-N-spread.tex |\
        sed 's/\\setlength[{]\\totalCoverWidth[}][{][^}]\+[}]/\\setlength{\\totalCoverWidth}{'$w'pt}/' |\
        sed 's/cover-1-spine/cover-'$n'-spine/' |\
        sed 's/cover-1-front/cover-'$n'-front/' > $name.tex

    lualatex -interaction=nonstopmode -halt-on-error -file-line-error $name.tex

    rm $name.tex $name.log $name.aux
done
