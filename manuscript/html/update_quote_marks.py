#!/usr/bin/env python3

import sys
import re
from pathlib import Path

def update_quote_marks_markdown(text: str) -> str:
    # One word, possibly with punctuation: "earth," -> 'earth',
    text = re.sub(r'"([\w-]+)([\.,:;\?]?)"', r"'\1'\2", text, flags=re.DOTALL|re.MULTILINE)

    # Two words:
    text = re.sub(r'"([\w-]+)[ \n]+([\w-]+)([\.,:;\?]?)"', r"'\1 \2'\3", text, flags=re.DOTALL|re.MULTILINE)

    # Three words:
    text = re.sub(r'"([\w-]+)[ \n]+([\w-]+)[ \n]+([\w-]+)([\.,:;\?]?)"', r"'\1 \2 \3'\4", text, flags=re.DOTALL|re.MULTILINE)

    return text

def update_quote_marks_latex(text: str) -> str:
    text = re.sub(r"``([\w-]+)([\.,:;\?]?)''", r"`\1'\2", text, flags=re.DOTALL|re.MULTILINE)

    text = re.sub(r"``([\w-]+)[ \n]+([\w-]+)([\.,:;\?]?)''", r"`\1 \2'\3", text, flags=re.DOTALL|re.MULTILINE)

    text = re.sub(r"``([\w-]+)[ \n]+([\w-]+)[ \n]+([\w-]+)([\.,:;\?]?)''", r"`\1 \2 \3'\4", text, flags=re.DOTALL|re.MULTILINE)

    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: update_quote_marks.py <files...(.md|.tex)>")

    for i in sys.argv[1:]:

        input_text_file = Path(i)
        output_text_file = input_text_file.with_stem(f"{input_text_file.stem}_edit")

        upd_text = ""

        with open(input_text_file, 'r', encoding='utf-8') as f:
            text = f.read()
            if input_text_file.suffix == ".md":
                upd_text = update_quote_marks_markdown(text)
            elif input_text_file.suffix == ".tex":
                upd_text = update_quote_marks_latex(text)
            else:
                print("Error: text file must be .md or .tex")
                sys.exit(1)

        with open(output_text_file, 'w', encoding='utf-8') as f:
            f.write(upd_text)
