from micropython import const
from time import sleep_ms
import ustruct

BUSY = const(1)  # 1=busy, 0=idle
EPD_WIDTH = 880
EPD_HEIGHT = 528

class EPD:
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.rotate = 0

    def _command(self, command, data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def init(self):
        self.reset()

        self._command(const(0x12))
        self.wait_until_idle()

        self._command(const(0x46))
        self._data(const(0xF7))
        self.wait_until_idle()

        self._command(const(0x47))
        self._data(const(0xF7))
        self.wait_until_idle()

        self._command(const(0x0C))
        self._data(const(0xAE))
        self._data(const(0xC7))
        self._data(const(0xC3))
        self._data(const(0xC0))
        self._data(const(0x40))
        
        self._command(const(0x01))
        self._data(const(0xAF))
        self._data(const(0x02))
        self._data(const(0x01))

        self._command(const(0x11))
        self._data(const(0x01))

        self._command(const(0x44))
        self._data(const(0x00))
        self._data(const(0x00))
        self._data(const(0x6F))
        self._data(const(0x03))
        self._command(const(0x45))
        self._data(const(0xAF))
        self._data(const(0x02))
        self._data(const(0x00))
        self._data(const(0x00))

        self._command(0x3C)
        self._data(0x01)

        self._command(const(0x18))
        self._data(const(0x80))
        self._command(const(0x22))
        self._data(const(0xB1))
        self._command(const(0x20))
        self.wait_until_idle()

        self._command(const(0x4E))
        self._data(const(0x00))
        self._data(const(0x00))
        self._command(const(0x4F))
        self._data(const(0xAF))
        self._data(const(0x02))
        self.wait_until_idle()


    def wait_until_idle(self):
        while self.busy.value() == BUSY:
            sleep_ms(100)

    def reset(self):
        self.rst(0)
        sleep_ms(200)
        self.rst(1)
        sleep_ms(200)

    def sleep(self):
        self._command(const(0x10))
        self._data(const(0x01))


    def display(self, imageblack, imagered):
        self._command(0x4F)
        self._data(0xAf)

        self._command(0x26)
        for i in range(0, int(self.width * self.height / 8)):
            self._data(~imagered[i])

        self._command(0x24)
        for i in range(0, int(self.width * self.height / 8)):
            self._data(imageblack[i])
            
        self._command(0x22)
        self._data(0xC7)
        self._command(0x20)
        sleep_ms(200)
        self.wait_until_idle()
        

    def Clear(self, color):
        if color == "black":
            c24 = 0x00
            c26 = 0x00
        elif color == "red":
            c24 = 0xff
            c26 = 0xff
        elif color == "white":
            c24 = 0xff
            c26 = 0x00

        self._command(0x4F)
        self._data(0xAf)
        
        self._command(0x24)
        for i in range(0, int(self.width * self.height / 8)):
            self._data(c24)
        
        
        self._command(0x26)
        for i in range(0, int(self.width * self.height / 8)):
            self._data(c26)
        
        self._command(0x22)
        self._data(0xC7) 
        self._command(0x20)
        sleep_ms(200)      #!!!The delay here is necessary, 200uS at least!!!     
        self.wait_until_idle()

        
    def set_pixel(self, frame_buffer, x, y, colored):
        if (x < 0 or x >= self.width or y < 0 or y >= self.height):
            return
        if (self.rotate == 0):
            self.set_absolute_pixel(frame_buffer, x, y, colored)


    def set_absolute_pixel(self, frame_buffer, x, y, colored):
        if (x < 0 or x >= EPD_WIDTH or y < 0 or y >= EPD_HEIGHT):
            return
        if (colored):
            frame_buffer[int((x + y * EPD_WIDTH) / 8)] &= ~(0x80 >> (x % 8))
        else:
            frame_buffer[int((x + y * EPD_WIDTH) / 8)] |= 0x80 >> (x % 8)


    def draw_char_at(self, frame_buffer, x, y, char, font, colored):
        char_offset = (ord(char) - ord(' ')) * font.height * (int(font.width / 8) + (1 if font.width % 8 else 0))
        offset = 0

        for j in range(font.height):
            for i in range(font.width):
                if font.data[char_offset+offset] & (0x80 >> (i % 8)):
                    self.set_pixel(frame_buffer, x + i, y + j, colored)
                if i % 8 == 7:
                    offset += 1
            if font.width % 8 != 0:
                offset += 1


    def display_string_at(self, frame_buffer, x, y, text, font, colored):
        refcolumn = x

        for index in range(len(text)):
            self.draw_char_at(frame_buffer, refcolumn, y, text[index], font, colored)
            refcolumn += font.width


    def draw_horizontal_line(self, frame_buffer, x, y, width, colored):
        for i in range(x, x + width):
            self.set_pixel(frame_buffer, i, y, colored)


    def draw_vertical_line(self, frame_buffer, x, y, height, colored):
        for i in range(y, y + height):
            self.set_pixel(frame_buffer, x, i, colored)


    def draw_rectangle(self, frame_buffer, x0, y0, x1, y1, colored):
        min_x = x0 if x1 > x0 else x1
        max_x = x1 if x1 > x0 else x0
        min_y = y0 if y1 > y0 else y1
        max_y = y1 if y1 > y0 else y0
        self.draw_horizontal_line(frame_buffer, min_x, min_y, max_x - min_x + 1, colored)
        self.draw_horizontal_line(frame_buffer, min_x, max_y, max_x - min_x + 1, colored)
        self.draw_vertical_line(frame_buffer, min_x, min_y, max_y - min_y + 1, colored)
        self.draw_vertical_line(frame_buffer, max_x, min_y, max_y - min_y + 1, colored)


    def draw_filled_rectangle(self, frame_buffer, x0, y0, x1, y1, colored):
        min_x = x0 if x1 > x0 else x1
        max_x = x1 if x1 > x0 else x0
        min_y = y0 if y1 > y0 else y1
        max_y = y1 if y1 > y0 else y0
        for i in range(min_x, max_x + 1):
            self.draw_vertical_line(frame_buffer, i, min_y, max_y - min_y + 1, colored)

    
    def draw_picture(self, framebuffer, pic_array):
        for i in range(self.height):
            for j in range(self.width//8):
                framebuffer[i*self.width//8 + j] = pic_array[i*self.width//8 + j]


    def draw_small_picture(self, framebuffer, pic_array, x, y, pic_height, pic_width):
        for i in range(pic_height):
            for j in range(pic_width//8):
                framebuffer[(i+y)*self.width//8 + j + x//8] = pic_array[i*pic_width//8 + j]

    def display_text(self, frame, x, y, data, font):
        display_word = ""
        index = 0
        for word in data.split():
            if len(display_word) > int(x*(-0.05)+48):
                self.display_string_at(frame, x, y+index*30, display_word, font, 1)
                display_word = word + " "
                index += 1
            else:
                display_word += word + " " 
        self.display_string_at(frame, x, y+index*30, display_word, font, 1)