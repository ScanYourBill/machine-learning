"""
Generate sales receipts images from a CSV file.

This script reads sales data from a CSV file, groups the data by receipt ID,
and generates an image for each receipt. Each receipt includes header information,
item details, and a total price.

Parameters:
- csv_filename: The filename of the CSV file containing sales data.

Returns:
- Image files representing the generated receipts.
"""

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


# Function to draw text with word wrap
def draw_text(draw, text, position, font, max_width):
    """
    Draw text with word wrap.

    Parameters:
    - draw: The ImageDraw object.
    - text: The text to draw.
    - position: The position to start drawing text.
    - font: The font to use for drawing text.
    - max_width: The maximum width for each line.

    Returns:
    - The y-coordinate after drawing the text.
    """
    
    lines = []
    if draw.textsize(text, font=font)[0] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and draw.textsize(line + words[i], font=font)[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            lines.append(line)

    y = position[1]
    for line in lines:
        draw.text((position[0], y), line, font=font, fill='black')
        y += font.getsize(line)[1]

    return y


# Load the CSV file
csv_filename = 'receipts10.csv'
receipts_df = pd.read_csv(csv_filename)

# Group the data by Receipt ID
grouped = receipts_df.groupby('Receipt ID')

# Create a template for the receipts
font_path = "arial.ttf"  # Path to a TTF font file, ensure this font file is available
font = ImageFont.truetype(font_path, 20)
header_font = ImageFont.truetype(font_path, 24)
total_font = ImageFont.truetype(font_path, 24)
image_width = 600
margin = 20
line_height = 30

# Generate an image for each receipt
for receipt_id, items in grouped:
    receipt_height = (len(items) + 5) * line_height + 5 * margin
    image = Image.new('RGB', (image_width, receipt_height), 'white')
    draw = ImageDraw.Draw(image)

    # Draw header
    y = margin
    # Draw company logo (optional)
    logo_path = "indomaret_logo.png"  # Path to a logo file
    try:
        logo = Image.open(logo_path)
        logo.thumbnail((200, 200))
        image.paste(logo, (margin + 180, margin))
    except IOError:
        print(f"Logo file not found at {logo_path}, skipping logo.")
    y += line_height + 50
    draw.text((margin, y), f"{'JL. WR. SUPRATMAN, LABUHANBATU':^65}", font=font, fill='black')
    y += line_height
    draw.text((margin, y), '-' * 80, font=font, fill='black')
    y += line_height
    draw.text((margin, y), f"{'16.06.18-17:00'}", font=font, fill='black')
    draw.text((margin, y), f"{'1.6.24':^85}", font=font, fill='black')
    draw.text((margin + 380, y), f"{'031153/JOKO/5501'}", font=font, fill='black')
    y += line_height
    draw.text((margin, y), '-' * 80, font=font, fill='black')
    y += line_height

    # Draw items
    for i, (index, item) in enumerate(items.iterrows()):
        if i < len(items) - 1:  # Check if it's not the last line
            draw.text((margin, y), item['Item'], font=font, fill='black')
            draw.text((margin + 250, y), "{:.0f}".format(item['Quantity']), font=font, fill='black')
            draw.text((margin + 325, y), "{:,.0f}".format(item['Price']), font=font, fill='black')
            draw.text((margin + 450, y), "{:,.0f}".format(item['Item Total']), font=font, fill='black')
            y += line_height


    # Draw total
    total = items[items['Item'] == 'TOTAL']['Item Total'].values[0]
    draw.text((margin + 250, y), '-' * 44, font=font, fill='black')
    y += line_height
    draw.text((margin + 250, y), "Total:", font=total_font, fill='black')
    draw.text((margin + 450, y), "{:,.0f}".format(total), font=total_font, fill='black')

    # Save the image
    image_filename = f"data/receipt_{int(receipt_id):02d}.jpg"
    image.save(image_filename)

print("Receipt images generated.")
