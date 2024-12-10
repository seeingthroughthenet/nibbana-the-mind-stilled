#!/usr/bin/env python3

import re
import subprocess
from typing import TypedDict

# cat nibbana-utf-8.html | sed 's/&#/\n&/g' | grep -E '&#[0-9]+;' | sed 's/\(&#[0-9]\+;\).*/\1/' | sort | uniq

HTML_TO_UNICODE = {
    "&#256;": "Ā",
    "&#257;": "ā",
    "&#299;": "ī",
    "&#347;": "ś",
    "&#363;": "ū",
    "&#57407;": "–", # shows a dash in the PDF, use en-dash
    "&#7693;": "ḍ",
    "&#7717;": "ḥ",
    "&#7735;": "ḷ",
    "&#7747;": "ṃ",
    "&#7749;": "ṅ",
    "&#7751;": "ṇ",
    "&#7771;": "ṛ",
    "&#7779;": "ṣ",
    "&#7789;": "ṭ",
    "&#8210;": "–", # ‒ Figure Dash, use en-dash
    "&#8213;": "–", # ― Horizontal Bar, use en-dash
}

class TextDict(TypedDict):
    text: str

def re_sub(pattern, repl, text: TextDict):
    """
    Performs the pattern replacement "in-place" on the 'text' key of the dict.
    """
    text['text'] = re.sub(pattern, repl, text['text'], flags=re.MULTILINE|re.DOTALL)

def convert_html_to_markdown(html_content: str) -> str:
    command = ["pandoc", "--wrap=none", "-f", "html", "-t", "markdown"]

    try:
        # Execute the command and capture output
        result = subprocess.Popen(command,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)

        # Pass the HTML content as input and get the output
        markdown_content, error_message = result.communicate(input=html_content)

        # Check if there were any errors
        if error_message:
            raise Exception(f"Pandoc conversion failed: {error_message}")

        return markdown_content.strip()

    except subprocess.SubprocessError as e:
        print(f"An error occurred while running pandoc: {e}")
        return ""

def convert():
    """
    Convert the UTF-8 HTML to Markdown with footnote syntax.
    """

    """
    https://seeingthroughthenet.net/wp-content/uploads/2018/03/Mind-Stilled_HTML.htm

    HTML downloaded is encoding charset=windows-1252

    iconv -f windows-1252 -t utf-8 -o nibbana-utf-8.html nibbana-windows-1252.html
    """

    html = TextDict(text="")
    with open('nibbana-utf-8.html', 'r', encoding='utf-8') as f:
        html['text'] = f.read()

    # <span lang=ZH-TW>ò</span>hit<span lang=ZH-TW>&#257;</span>
    # Ṭhitā
    html['text'] = html['text'].replace('<span lang=ZH-TW>ò</span>', 'Ṭ')

    html['text'] = html['text'].replace('&nbsp;', ' ')

    # Fix space in italics:
    # the<i> Dhamma</i> is
    # the <i>Dhamma </i>is
    re_sub(r'<i>\s+', ' <i>', html)
    re_sub(r'\s+</i>', '</i> ', html)

    # </span>ra-</i>element
    re_sub(r'-</i>(\w)', r'</i>-\1', html)

    # Fix possessive lowercase Arahant's here
    html['text'] = html['text'].replace("<i>Arahant's</i>", "<i>arahant's</i>")

    # Remove superfluous HTML

    html['text'] = html['text'].replace('<body bgcolor="#FFCC66" lang=EN-GB link=blue vlink=purple>', '<body>')
    html['text'] = html['text'].replace('<div class=Section1>', '<div>')

    re_sub(r'<style>(.*?)</style>', '', html)

    # TOC as a table
    re_sub(r'<table[^>]+>(.*?)</table>', '', html)

    # <p class=MsoNormal style='text-indent:14.2pt'>
    re_sub(r'<p class=[^>]+>', '<p>', html)

    # <hr size=1 width="33%" align=left>
    re_sub(r'<hr[^>]*>', '', html)

    for k, v in HTML_TO_UNICODE.items():
        html['text'] = html['text'].replace(k, v)

    re_sub(r'<span[^>]+>(.*?)</span>', r'\1', html)
    re_sub(r'<span[^>]+>(.*?)</span>', r'\1', html)
    re_sub(r'<span[^>]+>(.*?)</span>', r'\1', html)
    re_sub(r'<span[^>]+>(.*?)</span>', r'\1', html)

    # <div class=MsoNormal> </div>
    re_sub(r'<div class=MsoNormal>[\s\n]+</div>', '', html)

    # For inspecting the HTML result before Markdown conversion.
    # with open('nibbana-utf-8-unicode.html', 'w', encoding='utf-8') as f:
    #     f.write(html['text'])

    # Convert to markdown

    md = TextDict(text=convert_html_to_markdown(html['text']))

    # non-breaking space to regular space
    md['text'] = md['text'].replace('\u00A0', ' ')
    # niggahita
    md['text'] = md['text'].replace('ṃ', 'ṁ')
    md['text'] = md['text'].replace('Ṃ', 'Ṁ')

    # Use unicode en-dash
    md['text'] = md['text'].replace(' -- ', ' – ')
    md['text'] = md['text'].replace(' - ', ' – ')

    md['text'] = md['text'].replace('sotāpannā', 'sotāpanna')

    # Lowercase arahant. Include the italic syntax to exclude titles:
    # *Arahantavagga*
    # *Arahantsutta*
    for w in ["*Arahant*", "*Anāgāmi*", "*Sotāpanna*", "*Bodhisatta*"]:
        md['text'] = md['text'].replace(w, w.lower())

    # Plural forms:
    for w in ["*Arahants*", "*Anāgāmis*", "*Sotāpannas*", "*Bodhisattas*"]:
        md['text'] = md['text'].replace(w, w.lower())

    # Exception when 'Arahant' is used as a title, like Venerable:
    # Venerable *arahant* Subhūti -> Venerable Arahant Subhūti
    md['text'] = md['text'].replace('Venerable *arahant* Subhūti', 'Venerable Arahant Subhūti')

    md['text'] = md['text'].replace('*arahant*-ship', '*arahantship*')
    md['text'] = md['text'].replace("*Arahant-*ship", '*arahantship*')
    md['text'] = md['text'].replace('*arahant*-hood', '*arahanthood*')

    # Remove italics from common terms
    # Keep in mind punctuation: ... to see them in *Nibbāna.*
    for w in ["Nibbāna", "Buddha", "Dhamma", "Saṅgha", "Pāli", "sutta", "suttas"]:
        re_sub(r'\*' + w + r"([\.,:;\!\?\'-]*)\*",
               w + r'\1',
               md)

    """
    \"What is the \'two\'?\"

    \"Name and form.\"
    """
    re_sub(r'\\"', r'"', md)
    re_sub(r"\\'", r"'", md)

    """
    <div> </div>

    ** **

    *\
    *

    * *
    """

    md['text'] = md['text'].replace('<div>', '')
    md['text'] = md['text'].replace('</div>', '')
    md['text'] = md['text'].replace('\n** **\n', '\n')
    md['text'] = md['text'].replace('\n*\\\n*\n', '\n')
    md['text'] = md['text'].replace('\n* *\n', '\n')

    """
    \\
    """
    md['text'] = md['text'].replace('\n\\\n', '\n')

    # [back to top](#top)
    md['text'] = md['text'].replace('[back to top](#top)', '')

    # [**MIND STILLED**]{#Mindstilled02} **02**
    re_sub(r'\n\[\*\*MIND STILLED\*\*\]\{#Mindstilled[0-9]+\} *\*\*([0-9]+)\*\*\n', r'\n## Sermon \1\n', md)

    # HTML footnote clean-up

    """
    that it can be understood by the wise each one by himself.<a name="_ednref2"></a><a
    href="#_edn2" title="">[2]</a></p>

    ======

    <div id=edn2>

    <p><a name="_edn2"></a><a href="#_ednref2" title="">[2]</a> D II 93, <i>MahāParinibbānasutta</i>.</p>

    </div>

    ======

    Converted to Markdown:

    that it can be understood by the wise each one by himself.[]{#_ednref2}[\\[2\\]](#_edn2)

    ::: {#edn2}
    []{#_edn2}[\\[2\\]](#_ednref2) D II 93, *MahāParinibbānasutta*.
    :::
    """

    # Remove the back-reference links.
    re_sub(r'\[\]\{#_ednref[0-9]+\}', '', md)
    re_sub(r'^::: \{#edn[0-9]+\}\n(.*?)\n:::\n', r'\1\n', md)
    re_sub(r'\[\\\[([0-9]+)\\\]\]\(#_ednref[0-9]+\)', r'[\1]', md)

    """
    that it can be understood by the wise each one by himself.[\\[2\\]](#_edn2)

    []{#_edn2}[2] D II 93, *MahāParinibbānasutta*.
    """

    # Convert to Markdown footnote syntax

    # [\\[2\\]](#_edn2) -> [^fn2]
    re_sub(r'\[\\\[[0-9]+\\\]\]\(#_edn([0-9]+)\)', r'[^fn\1]', md)

    # []{#_edn2}[2] D II 93 -> [^fn2]: D II 93
    re_sub(r'\[\]\{#_edn([0-9]+)\}\[[0-9]+\] *([^\n]+)\n', r'[^fn\1]: \2\n', md)

    # Hyphen for numerical ranges: Dhp 92-93
    re_sub(r'([0-9]) *[-–] *([0-9])', r'\1-\2', md)

    # Remove trailing spaces
    re_sub(r'\s+$', r'\n', md)

    # Remove double blanks
    re_sub(r'\n\n\n+', r'\n\n', md)

    with open('nibbana.md', 'w', encoding='utf-8') as f:
        f.write(md['text'].strip())

if __name__ == "__main__":
    convert()
