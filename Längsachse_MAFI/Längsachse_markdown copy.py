from markdownmaker.document import Document
from markdownmaker.markdownmaker import *

# Create a new Markdown document
doc = Document()

# Add the image with the correct file path
image_path = "C:/Users/daka/Documents/Längsachse_MAFI/cedes_logo_mit_claim_rgb_1.png"
doc.add(Image(image_path, alt_text="Your Image Alt Text"))

# Add the section with a headline
doc.add(Header("Längsachsenmessung"))

# Add the table
table_data = [
    ["Distanz in [m]", "Grad in [°]"],
    [1, 2],
    [4, 5],
    [6, 7]
]
table_str = "\n".join([" | ".join(map(str, row)) for row in table_data])

# Add the table to the document
doc.add(table_str)



# Add the "halo" section
doc.add("**halo**")

# Save the Markdown document to a file
with open("output.md", "w", encoding="utf-8") as file:
    file.write(str(doc))