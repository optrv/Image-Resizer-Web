#!/usr/bin/env python3
import cgi
import os
from PIL import Image

print("Content-type: text/html")
print("<meta charset=\"utf-8\">")
print()
print("<style>h1,p{text-align:center;}</style>")

# Get the data
field = cgi.FieldStorage()
path_in = field.getfirst("path_in")
width = field.getfirst("width")
path_out = field.getfirst("path_out")
path_water = field.getfirst("path_water")
pos_water = field.getfirst("pos_water")

# Check if options are exist
if path_in is None:
    path_in = "/Users/garazd/Documents/Python/Img_In/"
if path_out is None:
    path_out = "/Users/garazd/Documents/Python/Img_Out/"
if width is None:
    width = 600
if path_water is None:
    path_water = "/Users/garazd/Documents/Python/Watermark/"
if pos_water is None:
    pos_water = 4 # The default value of watermark position — right below

folder_in = os.listdir(path_in)
folder_water = os.listdir(path_water)

# Watermark adding with specified (or default) value of position on image
def watermark(image_out, pos_water):
    for files in folder_water:
        if files.endswith('png') or files.endswith('jpg'):
            water = Image.open(os.path.join(path_water, files))
            if water.mode != 'RGBA':
                water = water.convert('RGBA')
            water = water.resize((image_out.size[0] // 4, \
            int((image_out.size[0] // 4 * water.size[1]) // water.size[0])), Image.BILINEAR)
            layer = Image.new('RGBA', image_out.size, (0, 0, 0, 0))
            place = {1: (10, 10), 2: (image_out.size[0] - 10 - water.size[0], 10), 3: (10, \
                    image_out.size[1] - 10 - water.size[1]), 4: (image_out.size[0] - 10 - \
                    water.size[0], image_out.size[1] - 10 - water.size[1])}
            pos_water = (place[int(pos_water)])
            layer.paste(water,(pos_water))
            image_out = Image.composite(layer, image_out, layer)
            break # Just first one watermark image in the specified folder
    return image_out

print()
for image_in in folder_in:
    if not image_in.startswith('.') and image_in != 'Thumbs.db':
        print('Resizing image' + ' ' + image_in)
        image_out = Image.open(os.path.join(path_in, image_in))
        if image_out.mode != 'RGBA':
            image_out = image_out.convert('RGBA')

        # Resize image proportional to specified width
        image_out = image_out.resize((width, int((width * image_out.size[1]) / \
                    image_out.size[0])), Image.BILINEAR)

        # Save image. Make output-folder if it's not exists
        if not os.path.exists(path_out):
            os.makedirs(path_out)
            if path_water is not None and pos_water is not None:
                image_out = watermark(image_out, pos_water)
                image_out.save(os.path.join(path_out, 'resized+watermark-' + image_in))
            else:
                image_out.save(os.path.join(path_out, 'resized-' + image_in))
        # Just save image
        else:
            if path_water is not None and pos_water is not None:
                image_out = watermark(image_out, pos_water)
                image_out.save(os.path.join(path_out, 'resized+watermark-' + image_in))
            else:
                image_out.save(os.path.join(path_out, 'resized-' + image_in))
print()
print('Batch resizing (& watermarking) processing complete.')
