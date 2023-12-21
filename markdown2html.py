#!/usr/bin/python3
"""markdown2html"""

import sys
import os


def convert_markdown_to_html(input_md_file, output_html_file):
    with open(input_md_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    html_lines = []

    # Split the Markdown content into lines
    lines = markdown_content.split('\n')

    for line in lines:
        # Check for headings
        if line.startswith("#"):
            heading_level = line.count("#")
            heading_text = line.lstrip("#").strip()
            html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
        else:
            # Preserve line breaks and treat other lines as paragraphs
            if line.strip():  # Ignore empty lines
                html_lines.append(line)

    # Combine lines into HTML
    html_content = "\n".join(html_lines) + "\n"  # Add a newline at the end

    with open(output_html_file, 'w', encoding='utf-8') as file:
        file.write(html_content)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_md_file = sys.argv[1]
    output_html_file = sys.argv[2]

    if not os.path.isfile(input_md_file):
        sys.stderr.write(f"Error: Missing {input_md_file}\n")
        sys.exit(1)

    convert_markdown_to_html(input_md_file, output_html_file)
