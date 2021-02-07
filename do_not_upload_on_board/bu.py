import time

def read_rows(path):

    image_file = open(path, "rb")
    # Blindly skip the BMP header.
    image_file.seek(54)

    # We need to read pixels in as rows to later swap the order
    # since BMP stores pixels starting at the bottom left.
    rows = []
    row = []
    buf = 0
    buf_len = 0
    pixel_index = 0
    # print(len(image_file.read()))
    while True:
        if pixel_index == 880:
            pixel_index = 0
            rows.insert(0, row)
            row = []
        pixel_index += 1

        r_string = image_file.read(3)

        if len(r_string) == 0:
            break

        r = r_string[0]

        if r >= 130:
            r = 1
        else:
            r = 0

        buf = buf + (r << buf_len)
        buf_len += 1
        if buf_len == 8:
            row.append(buf)
            buf_len = 0
            buf = 0

    image_file.close()
    return rows

def repack_sub_pixels(rows):
    print("Repacking pixels...")
    xd = 0
    sub_pixels = []
    for row in rows:
        # print(row)
        # for sub_pixel in row:
        #     sub_pixels.append(sub_pixel)

    return sub_pixels

f_name = "rsz_osk.bmp"
rows = read_rows(f_name)
sub_pixels = repack_sub_pixels(rows)

f = open('data.txt', 'w')
f.write(f_name[:-4] + " = " + str(bytearray(sub_pixels)))
f.close()

print("AAA")
print(len(bytearray(sub_pixels)))
print("AAA")
print(bytearray(sub_pixels))