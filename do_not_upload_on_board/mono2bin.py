from PIL import Image
import os


height = 528            #fill
width = 880             #fill
buf = [0xFF] * (int(width / 8) * height)

image = Image.open(os.path.join('osk.bmp'))
image_monocolor = image.convert('1')
imwidth, imheight = image_monocolor.size
pixels = image_monocolor.load()

if(imwidth == width and imheight == height):
    for y in range(imheight):
        for x in range(imwidth):
            if pixels[x, y] == 0:
                buf[int((x + y * width) / 8)] &= ~(0x80 >> (x % 8))
elif(imwidth == height and imheight == width):
    for y in range(imheight):
        for x in range(imwidth):
            newx = y
            newy = height - x - 1
            if pixels[x, y] == 0:
                buf[int((newx + newy*width) / 8)] &= ~(0x80 >> (y % 8))

print(len(buf))
print(buf)
print(bytearray(buf))