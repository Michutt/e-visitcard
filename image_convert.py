import uos


def convert_image(path):
    image_file = open(path, "rb")
    image_file.seek(54)

    row = []
    buf = 0
    buf_len = 8
    pixel_index = 0
    xd = 0
    sub_pixels = []
    while True:
        if pixel_index == 880:
            pixel_index = 0
            sub_pixels = row + sub_pixels
            row = []
            xd += 1
        pixel_index += 1

        r_string = image_file.read(3)

        if len(r_string) == 0:
            break

        r = r_string[0]

        if r >= 110:
            r = 1
        else:
            r = 0

        buf_len -= 1
        buf = buf + (r << buf_len)
        if not buf_len:
            row.append(buf)
            buf_len = 8
            buf = 0

    image_file.close()
    return bytearray(sub_pixels)

def save_image(byte_image, f_name):
    f_name = f_name[:-4]
    f = open('images/generated/' + f_name + '.py', 'w')
    f.write(f_name + " = " + str(byte_image))
    f.close()

def generate_new_files():
    uos.chdir("images/generated")
    files = uos.listdir()
    uos.chdir("/flash")
    files1 = uos.listdir()
    for file in files:
        if file[-4:] == ".bmp":
            byte_image = convert_image("images/generated/" + file)
            save_image(byte_image, file)