from PIL import Image, ImageDraw, ImageFont

# Takes 2 images, one is a texture, another is just 0,0,0 and 255,255,255 image.
# The texture is applied to the other image where there are 255

texture = Image.open('gold1.jpg') # 2590x1940

# Create image with a font
font_path = './2021-chakobsa.ttf'
font = ImageFont.truetype(font_path, 400)
image = Image.new('RGB', (2590, 1940), (0, 0, 0))
draw = ImageDraw.Draw(image)
draw.text((50, 50), 'Hello, World!', font=font, fill=(255, 255, 255))


def apply_texture(texture, image):
    texture = texture.convert('RGBA')
    image = image.convert('RGBA')
    texture_data = texture.getdata()
    image_data = image.getdata()
    new_data = []
    for i in range(len(image_data)):
        if image_data[i][0] == 255:
            new_data.append(texture_data[i])
        else:
            new_data.append(image_data[i])
    image.putdata(new_data)
    return image

image = apply_texture(texture, image)

image.save('result.png')

