import random
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


# This script generates random receipt images using data from a CSV file.
# It uses the PIL library to draw text and images onto a blank canvas to simulate a receipt.
# The receipts include a logo, header information, and a list of items with their prices and quantities.

def draw_text(draw, text, position, font, max_width):
    """
    Draws text within a specified width on an image.

    :param draw: ImageDraw object to draw on the image.
    :param text: The text to be drawn.
    :param position: Tuple (x, y) where the text will start.
    :param font: The font of the text.
    :param max_width: The maximum width allowed for the text.
    :return: The y position after the text is drawn.
    """
    lines = []
    # Split the text into lines that fit within the max_width
    if draw.textsize(text, font=font)[0] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        line = ''
        for word in words:
            if draw.textsize(line + word, font=font)[0] <= max_width:
                line += word + ' '
            else:
                lines.append(line)
                line = word + ' '
        lines.append(line)

    y = position[1]
    # Draw each line on the image
    for line in lines:
        draw.text((position[0], y), line, font=font, fill='black')
        y += font.getsize(line)[1]

    return y


def generate_random_receipts(list_items, num_receipts, font_path, logo_path):
    """
    Generates random receipt images with varying items and quantities.

    :param list_items: A list of dictionaries containing item details.
    :param num_receipts: The number of receipts to generate.
    :param font_path: Path to the font file used for drawing text.
    :param logo_path: Path to the logo image file.
    """

    # Load fonts
    font = ImageFont.truetype(font_path, 20)
    total_font = ImageFont.truetype(font_path, 24)

    # Set image dimensions and styling parameters
    image_width = 800
    margin = 20
    line_height = 30

    # Generate each receipt image
    for receipt_id in range(1, num_receipts + 1):
        num_items = random.randint(1, 50)
        chosen_items = random.sample(list_items, num_items)
        total_price = 0

        # Calculate receipt height based on number of items
        receipt_height = (num_items + 6) * line_height + 6 * margin
        image = Image.new('RGB', (image_width, receipt_height), 'white')
        draw = ImageDraw.Draw(image)

        y = margin
        # Try to open and paste the logo onto the receipt
        try:
            logo = Image.open(logo_path)
            logo.thumbnail((200, 200))
            image.paste(logo, (margin + 278, margin))
        except IOError:
            print(f"Logo file not found at {logo_path}, skipping logo.")

        # Skip space for logo height
        y += line_height + 50

        # Header information for the receipt
        header_info = [
            f"{'JL. WR. SUPRATMAN, LABUHANBATU':^102}",
            '-' * 114,
            f"{'16.06.18-17:00'}{'1.6.24':^77}{'031153/JOKO/5501'}",
            '-' * 114
        ]

        # Draw header information on the receipt
        for info in header_info:
            draw.text((margin, y), info, font=font, fill='black')
            y += line_height

        # Draw each item with its quantity and price on the receipt
        for item in chosen_items:
            quantity = random.randint(1, 3)
            item_total = quantity * item['harga']
            total_price += item_total

            draw.text((margin, y), item['nama'], font=font, fill='black')
            draw.text((margin + 450, y), "{:.0f}".format(quantity), font=font, fill='black')
            draw.text((margin + 525, y), "{:,.0f}".format(item['harga']), font=font, fill='black')
            draw.text((margin + 650, y), "{:,.0f}".format(item_total), font=font, fill='black')
            y += line_height

        # Draw a line before the total
        draw.text((margin + 450, y), '-' * 46, font=font, fill='black')
        y += line_height

        # Draw the total price of all items
        draw.text((margin + 450, y), "Total:", font=total_font, fill='black')
        draw.text((margin + 630, y), "{:,.0f}".format(total_price), font=total_font, fill='black')

        # Save the receipt image with a unique filename
        image_filename = f"data/receipt_{receipt_id:02d}.jpg"
        image.save(image_filename)

    print("Receipt images generated.")

# Load data from a CSV file into a DataFrame and convert it to a list of dictionaries
receipts_df = pd.read_csv('data/data.csv')
list_of_dicts = receipts_df.to_dict('records')

# Parameters for receipt generation
font_path = "arial.ttf"  # Path to the font file
logo_path = "data/indomaret_logo.png"  # Path to the logo image file
num_receipts = 10  # Number of receipts to generate

# Generate random receipts images
generate_random_receipts(list_of_dicts, num_receipts, font_path, logo_path)