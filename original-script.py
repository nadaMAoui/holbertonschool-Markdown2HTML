#!/usr/bin/python3
"""markdown2html"""

import sys
import os


def process_ordered_list(lines):
    html_lines = ["<ol>"]

    for line in lines:
        list_item = line.split(". ", 1)[1].strip()
        html_lines.append(f"    <li>{list_item}</li>")

    html_lines.append("</ol>")
    return html_lines


def process_unordered_list(lines):
    html_lines = ["<ul>"]

    for line in lines:
        list_item = line.lstrip("- ").strip()
        html_lines.append(f"    <li>{list_item}</li>")
        
        # Close the <ul> tag if the next line does not start with "-" or is empty
        next_line = lines[lines.index(line) + 1]
        if not next_line.strip() or not next_line.lstrip().startswith("- "):
            html_lines.append("</ul>")
        
    return html_lines


def process_paragraph(lines):
    html_lines = ["<p>"]

    for line in lines:
        html_lines.append(f"    {line}")

    html_lines.append("</p>")
    return html_lines


def convert_markdown_to_html(input_md_file, output_html_file):
    with open(input_md_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    # Split the Markdown content into lines
    lines = markdown_content.split('\n')

    html_lines = []

    in_ordered_list = False
    in_unordered_list = False
    in_paragraph = False

    for line in lines:
        # Check for headings
        if line.startswith("#"):
            heading_level = line.count("#")
            heading_text = line.lstrip("#").strip()
            if in_ordered_list:
                in_ordered_list = False
                html_lines.append("</ol>")
            if in_unordered_list:
                in_unordered_list = False
                html_lines.append("</ul>")
            if in_paragraph:
                in_paragraph = False
                html_lines.append("</p>")
            html_lines.append(
                f"<h{heading_level}>{heading_text}</h{heading_level}>")

        elif line.startswith("* "):
            # Start or continue an unordered list
            if not in_unordered_list:
                in_unordered_list = True
                html_lines.append("<ul>")
            if in_ordered_list:
                in_ordered_list = False
                html_lines.append("</ol>")
            if in_paragraph:
                in_paragraph = False
                html_lines.append("</p>")
            html_lines.append(f"    <li>{line.lstrip('* ').strip()}</li>")

        elif line.lstrip().startswith("- "):
            # Start or continue an unordered list outside a paragraph
            if not in_unordered_list:
                in_unordered_list = True
                html_lines.append("<ul>")
            if in_ordered_list:
                in_ordered_list = False
                html_lines.append("</ol>")
            if in_paragraph:
                in_paragraph = False
                html_lines.append("</p>")
            html_lines.append(f"    <li>{line.lstrip('- ').strip()}</li>")
            
            # Close the <ul> tag if the next line does not start with "-" or is empty
            next_line = lines[lines.index(line) + 1]
            if not next_line.strip() or not next_line.lstrip().startswith("- "):
                html_lines.append("</ul>")
            
        elif line and line[0].isalpha():
            # Start or continue a paragraph for lines starting with a letter
            if not in_paragraph:
                in_paragraph = True
                html_lines.append("<p>")
            if in_unordered_list:
                in_unordered_list = False
                html_lines.append("</ul>")
            if in_ordered_list:
                in_ordered_list = False
                html_lines.append("</ol>")
            html_lines.append(f"    {line.strip()}")

        else:
            # If line is empty, close the paragraph if open
            if in_paragraph:
                in_paragraph = False
                html_lines.append("</p>")

    # Close any remaining lists or paragraphs
    if in_unordered_list:
        html_lines.append("</ul>")
    if in_ordered_list:
        html_lines.append("</ol>")
    if in_paragraph:
        html_lines.append("</p>")

    # Combine lines into HTML with each tag on a new line, excluding empty lines
    html_content = "\n".join(
        line for line in html_lines if line.strip()) + "\n"

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
