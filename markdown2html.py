#!/usr/bin/python3
"""markdown2html"""

import sys
import os


def process_unordered_list(lines):
    html_lines = ["<ul>"]

    for line in lines:
        list_item = line.lstrip("- ").strip()
        html_lines.append(f"    <li>{list_item}</li>")

    html_lines.append("</ul>")
    return html_lines


def convert_markdown_to_html(input_md_file, output_html_file):
    with open(input_md_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    # Split the Markdown content into lines
    lines = markdown_content.split('\n')

    html_lines = []

    in_list = False

    for line in lines:
        # Check for headings
        if line.startswith("#"):
            heading_level = line.count("#")
            heading_text = line.lstrip("#").strip()
            if in_list:
                in_list = False
                html_lines.append("</ul>")
            html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
        elif line.startswith("- "):
            # Start or continue an unordered list
            if not in_list:
                in_list = True
                html_lines.append("<ul>")
            html_lines.extend(process_unordered_list([line]))
        else:
            if in_list:
                in_list = False
                html_lines.extend(process_unordered_list([line]))
            else:
                html_lines.append(line)

    # Close the unordered list if still open
    if in_list:
        html_lines.append("</ul>")

    # Combine lines into HTML with each tag on a new line
    html_content = "\n".join(html_lines) + "\n"

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
