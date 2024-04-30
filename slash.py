# In the Discord Development portal, Make sure to add the "bot" and "application.commands" scopes in OAuth2 link generator
from dotenv import load_dotenv
import io
import os
from PIL import Image, ImageDraw, ImageFont

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

import discord

bot = discord.Bot()


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

@bot.event
async def on_ready():
    print(f'Bot is online and ready to go!')
    # await bot.sync_commands(delete_existing=True)
    await bot.change_presence(activity=discord.Game(name="Testing"), status=discord.Status.online)
                                                    # ^ change to your liking

# NOTE these are testing commands. Feel free to change them or add more.    
@bot.command(name="gliphify", description="Sends the bot's latency.") 
async def gliphify(ctx, text: discord.Option(str, "The text to gliphify")):
    orig = text
    # to lower case
    text = text.lower()

    # Maximum line length
    max_line_length = 800
    # Margins
    margin_left = 40
    margin_top = 10
    margin_right = 60
    margin_bottom = 20

    # Create a new image with a white background
    img = Image.new('RGB', (max_line_length + margin_left + margin_right, 150), color=(0, 0, 0))
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
    await ctx.respond(f'{orig}',file=file)



bot.run(bot_token)
