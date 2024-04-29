import discord
from PIL import Image, ImageDraw, ImageFont
import io

# dotenv
import os
from dotenv import load_dotenv

load_dotenv()

# bot token from en
bot_token = os.getenv("BOT_TOKEN")

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Load your custom font
font_path = './2021-chakobsa.ttf'
font_size = 100
font = ImageFont.truetype(font_path, font_size)

features = {
    'liga': 1, # Enable ligatures
    'calt': 1, # Enable contextual alternates
    'kern': 1, # Enable kerning
    'salt': 0   # Disable stylistic sets
}

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!chakobsa'):
        # remove !chakobsa from the message

        text = message.content[9:]
        orig = text
        # to lower case
        text = text.lower()

        # Maximum line length
        max_line_length = 800
        # Margins
        margin_left = 20
        margin_top = 20
        margin_right = 20
        margin_bottom = 20

        # Create a new image with a white background
        img = Image.new('RGB', (max_line_length + margin_left + margin_right, 100), color=(0, 0, 0))
        d = ImageDraw.Draw(img)

        # Calculate the width of the text
        bbox = d.textbbox((0, 0), text, font=font, features=features)
        text_width = bbox[2] - bbox[0]

        # If the text width exceeds the maximum line length, split it into lines
        if text_width > max_line_length:
            words = text.split()
            lines = []
            current_line = []
            current_line_width = 0

            for word in words:
                word_bbox = d.textbbox((0, 0), word, font=font, features=features)
                word_width = word_bbox[2] - word_bbox[0]
                if current_line_width + word_width <= max_line_length:
                    current_line.append(word)
                    current_line_width += word_width
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_line_width = word_width

            if current_line:
                lines.append(' '.join(current_line))

            # Adjust the image height based on the number of lines
            img_height = len(lines) * font_size + margin_top + margin_bottom
            img = Image.new('RGB', (max_line_length + margin_left + margin_right, img_height), color=(0, 0, 0))
            d = ImageDraw.Draw(img)

            # Render each line
            y = margin_top
            for line in lines:
                d.text((margin_left, y), line, font=font, fill=(255, 255, 255), features=features)
                y += font_size

        else:
            # Render the text if it fits within the maximum line length
            d.text((margin_left, margin_top), text, font=font, fill=(255, 255, 255), features=features)

        # Save the image to a BytesIO object
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Create a discord.File object and send it
        file = discord.File(fp=io.BytesIO(img_byte_arr), filename='rendered_text.png')
        await message.delete()
        mention = message.author.mention
        await message.channel.send(f'From: {mention}\n{orig}',file=file)


# Replace 'your_bot_token' with your actual bot token
client.run(bot_token)
