#!/usr/bin/env python3

import re
import csv
import glob
import os
import sys
from pathlib import Path
from typing import List, TypedDict

class RefData(TypedDict):
    PTS: str
    SC: str
    Title: str
    Comments: str

def sc_ref_uid(ref: str) -> str:
    # SN 20.7 -> sn20.7
    # SN 43.13-44 -> sn43.13
    uid = ref.lower().replace(" ", "")
    uid = re.sub("-.*", "", uid)
    return uid

def convert_references_in_file(ref_data: List[RefData], file_path: Path):
    text = ""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    if file_path.suffix == ".md":
        # [^fn3]: S II 267, *Āṇisutta*
        # to
        # [^fn3]: [SN 20.7 / S II 267](https://suttacentral.net/sn20.7/pli/ms), *Āṇisutta*

        # PTS can be a list: D II 90, D II 93, D II 157

        for i in ref_data:
            pts_refs = [x.strip() for x in i['PTS'].split(",")]
            for pts in pts_refs:
                # NOTE: \b needed: S I 12 should not match S I 121
                pat = re.compile(pts + r"\b([^]])", flags=re.MULTILINE)
                linked = r"[%s / %s](https://suttacentral.net/%s/pli/ms)\1" % (i['SC'], pts, sc_ref_uid(i['SC']))
                text = pat.sub(linked, text)

    elif file_path.suffix == ".tex":
        # \footnote{S II 267, \emph{Āṇisutta}}
        # to
        # \footnote{\href{https://suttacentral.net/sn20.7/pli/ms}{SN 20.7 / S II 267}, \emph{Āṇisutta}}

        for i in ref_data:
            pts_refs = [x.strip() for x in i['PTS'].split(",")]
            for pts in pts_refs:
                pat = re.compile(pts + r"\b([^}])", flags=re.MULTILINE)
                linked = r"\\href{https://suttacentral.net/%s/pli/ms}{%s / %s}\1" % (sc_ref_uid(i['SC']), i['SC'], pts)
                text = pat.sub(linked, text)

    else:
        raise Exception("Cannot handle file format: " + file_path.suffix)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    ref_data: List[RefData] = []

    with open(Path(__file__).parent.joinpath("pts_to_sc.tsv"), newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')
        ref_data = list(reader) # type: ignore

    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        manuscript_dir = Path(__file__).parent.parent.joinpath("manuscript")
        files = []
        files.extend(glob.glob(os.path.abspath(manuscript_dir.joinpath("markdown/sermon-*.md"))))
        files.extend(glob.glob(os.path.abspath(manuscript_dir.joinpath("tex/sermon-*.tex"))))

    print(f"Converting references in {len(files)} files...")

    for i in files:
        convert_references_in_file(ref_data, Path(i))
