#!/usr/bin/env python3

import re
from typing import List

def extract_names_from_markdown(file_path) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        md = file.read()

    # A name always starts with a capital letter.
    # A name is one or two words wrapped in italic.
    # *Ānanda*, *Assaji Thera*, *Sāmanera Sopāka*
    # The italic may include punctuation marks at the end, for example:
    # *Ānanda.* or *Ānanda'*.
    # The italic may include the possesive marker, for example:
    # *Ānanda's*

    pattern = r"\*([A-ZĀ]\w+ [A-ZĀ][\w\.:;\'\?\!]+|[A-ZĀ][\w\.:;\'\?\!]+)\*"

    uniq_names = list(set(re.findall(pattern, md)))

    def _maybe_name(s: str) -> bool:
        return re.search(r'(sutta|vagga|gāthā|nikāya|pucchā|saṁyutta)', s, flags=re.IGNORECASE) is None

    uniq_names = [i for i in uniq_names if _maybe_name(i)]

    uniq_names.sort()

    return uniq_names

if __name__ == "__main__":
    for i in extract_names_from_markdown("nibbana.md"):
        print(i)
