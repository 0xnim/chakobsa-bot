from PIL import Image, ImageDraw, ImageFont

# Load the target image and ensure it's in RGBA mode
target_image = Image.open('gold1.jpg').convert('RGBA')

# Create a new image with the same size as the target image for the mask
mask = Image.new('RGBA', target_image.size, (255, 255, 255, 255))

# Create a draw object for the mask
draw = ImageDraw.Draw(mask)

# Specify the font and size
font = ImageFont.truetype('./2021-chakobsa.ttf', 15)

# Draw the text on the mask image
draw.text((50, 50), "Hello World", font=font, fill=(0, 0, 0, 255))

# Invert the colors of the mask to create the alpha channel effect
mask = Image.alpha_composite(mask, Image.new('RGBA', mask.size, (255, 255, 255, 0)))

# Ensure the target image is in RGBA mode before applying putalpha
target_image = target_image.convert('RGBA')

# Apply the mask to the target image
target_image.putalpha(mask)

# Save the result
target_image.save('result.png')

