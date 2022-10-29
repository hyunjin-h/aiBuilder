from PIL import Image, ImageDraw

img = Image.open('image/input_photo.jpg').convert('RGB')

draw = ImageDraw.Draw(img)
draw.rectangle((0,0,640,480), outline=(0,255,0), width = 3)

img.show()