from tabulate import tabulate
import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


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

def markdown_to_pdf(md_string, output_path):
    # Convert Markdown to HTML
    html = markdown2.markdown(md_string)

    # Initialize a canvas
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Set font and draw HTML content on the canvas
    c.setFont("Helvetica", 12)  # Set font (adjust as needed)
    c.drawString(100, 750, html)

    # Save the PDF
    c.save()

# Example call with given data, title, text, and image path
distances = [1, 4, 6]
angles = [2, 5, 7]
measurements = list(zip(distances, angles))
title_line = "Längsachsenmessung"
text_above_table = "Hier ist eine Tabelle mit den Distanz- und Gradwerten:"
image_path = "C:/Users/daka/Documents/Längsachse_MAFI/cedes_logo_mit_claim_rgb_1.png"

# Generate Markdown content with table, title, text, and image
markdown_table_with_text_title_and_image = generate_table_with_text_and_title(measurements, title_line, text_above_table, image_path)

output_file = "output.pdf"


# Print the generated Markdown content
print(markdown_table_with_text_title_and_image)

markdown_to_pdf(markdown_table_with_text_title_and_image, output_file)
