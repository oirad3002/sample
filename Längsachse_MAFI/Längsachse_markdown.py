from tabulate import tabulate
import mdpdf
from weasyprint import HTML

def generate_table_with_text_and_title(measurements, title, text, image_path):
    # Create headers for the table
    headers = ['Distanz in [m]', 'Grad in [°]']

    # Generate Markdown table
    markdown_table = tabulate(measurements, headers, tablefmt="github")

    # Add title line
    title_line = f"## {title}\n\n"

    # Add text above the table
    text_above_table = f"{title_line}{text}\n\n"

    # Add image line
    image_line = f"![Your Image Alt Text]({image_path})\n\n"

    # Combine Markdown table with title, text, and image
    table_with_text_title_and_image = f"{image_line}{text_above_table}{markdown_table}"

    return table_with_text_title_and_image

# Example call with given data, title, text, and image path
distances = [1, 4, 6]
angles = [2, 5, 7]
measurements = list(zip(distances, angles))
title_line = "Längsachsenmessung"
text_above_table = "Hier ist eine Tabelle mit den Distanz- und Gradwerten:"
image_path = "C:/Users/daka/Documents/Längsachse_MAFI/cedes_logo_mit_claim_rgb_1.png"

# Generate Markdown content with table, title, text, and image
markdown_table_with_text_title_and_image = generate_table_with_text_and_title(measurements, title_line, text_above_table, image_path)

# Convert Markdown to HTML
with open('output.md', 'r') as f:
    markdown_content = f.read()
html_content = f"<html><body>{markdown_content}</body></html>"

# Convert HTML to PDF
HTML(string=html_content).write_pdf('output.pdf')

# Print the generated Markdown content
print(markdown_table_with_text_title_and_image)