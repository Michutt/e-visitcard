# imports from system libraries
from machine import Pin, SPI, deepsleep
from network import LoRa
import ubinascii
import socket
import pycom
import time
import gc

# imports from user files 
from pre_defined_displays import *
from image_convert import *
import epaper7in5b_HD

# disable RGB diode
pycom.heartbeat(False)

# set SPI pins
rst = Pin('P4')
dc = Pin('P20')
busy = Pin('P9')
cs = Pin('P3')
clk = Pin('P10')
mosi = Pin('P11')

# init SPI
spi = SPI(0, mode=SPI.MASTER, baudrate=500000, polarity=0, phase=0, pins=(clk, mosi, None))

# lora = LoRa(mode=LoRa.LORAWAN)
# lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

e = epaper7in5b_HD.EPD(spi, cs, dc, rst, busy)

# app_eui = ubinascii.unhexlify('70B3D549915AE2B8')
# app_key = ubinascii.unhexlify('F2C715A50B51C0ADBC4C7CD6675773F5')

# generate_new_files()

fb_size = int(e.width * e.height)
frame_black = bytearray(bytes([255]) * fb_size)
frame_red = bytearray(bytes([255]) * fb_size)

lista = [b'\x71\x11\x11\x01\x99\x02\x99\x00\x50', b'\xd1', b'\xdb', b'\xd1']
i = 0
while(True):
    gc.collect()
    # lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

    # # wait until the module has joined the network
    # join_time = 0
    # while join_time != 2 and not lora.has_joined():
    #     time.sleep(2)
    #     join_time += 2
    #     print('Not yet joined...')

    # # create a LoRa socket
    # s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # # set the LoRaWAN data rate
    # s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    # # make the socket blocking
    # s.setblocking(True)

    # time.sleep(8)
    # # make the socket non-blocking
    # # (because if there's no data received it will block forever...)
    # s.setblocking(False)

    # get any data received (if any...)
    # data = s.recv(64)
    for data in lista:
        print(data)
        e.init()

        # predefined images
        if hex(data[0]) == '0xaa':
            if hex(data[1]) == '0x11':
                template(frame_black, frame_red, e)
                first_screen(frame_black, frame_red, e)
            elif hex(data[1]) == '0x12':
                second_screen(frame_black, frame_red, e)
            elif hex(data[1]) == '0x13':
                template(frame_black, frame_red, e)
                third_screen(frame_black, frame_red, e)
            elif hex(data[1]) == '0x14':
                template(frame_black, frame_red, e)
                fourth_screen(frame_black, frame_red, e)
            elif hex(data[1]) == '0x15':
                template(frame_black, frame_red, e)
                fifth_screen(frame_black, frame_red, e)

        if hex(data[0]) == '0x22':
            elif hex(data[1]) == '0x11':
                template(frame_black, frame_red, e)

        # text display
        elif hex(data[0]) == '0x66':
            if hex(data[1]) == '0x11':
                font = font20
            elif hex(data[1]) == '0x12':
                font = font24
            
            x = (data[3]//16*10 + data[3]-data[3]//16*16)*100
            x = x + data[4]//16*10 + data[4]-data[4]//16*16
            y = (data[5]//16*10 + data[5]-data[5]//16*16)*100
            y = y + data[6]//16*10 + data[6]-data[6]//16*16
            text = data[7:].decode("utf-8")
            print(text)

            if hex(data[2]) == '0x11':
                e.display_string_at(frame_black, x, y, text, font, 1)
            elif hex(data[2]) == '0x12':
                e.display_string_at(frame_red, x, y, text, font, 1)

        # draw line
        elif hex(data[0]) == '0x71':
            x = (data[3]//16*10 + data[3]-data[3]//16*16)*100
            x = x + data[4]//16*10 + data[4]-data[4]//16*16
            y = (data[5]//16*10 + data[5]-data[5]//16*16)*100
            y = y + data[6]//16*10 + data[6]-data[6]//16*16
            width = (data[7]//16*10 + data[7]-data[7]//16*16)*100
            width = width + data[8]//16*10 + data[8]-data[8]//16*16

            if hex(data[1]) == '0x11':
                if hex(data[2]) == '0x11':
                    e.draw_horizontal_line(frame_black, x, y, width, 1)
                elif hex(data[2]) == '0x12':
                    e.draw_horizontal_line(frame_red, x, y, width, 1)

            elif hex(data[1]) == '0x12':
                if hex(data[2]) == '0x11':
                    e.draw_vertical_line(frame_black, x, y, width, 1)
                elif hex(data[2]) == '0x12':
                    e.draw_vertical_line(frame_red, x, y, width, 1)     
        
        # clear buffer
        elif hex(data[0]) == '0xff':
            if hex(data[1]) == '0x11':
                frame_black = bytearray(bytes([255]) * fb_size)
            if hex(data[1]) == '0x12':
                frame_red = bytearray(bytes([255]) * fb_size)
        
        # fill buffer with color
        elif hex(data[0]) == '0xfe':
            del frame_black
            del frame_red
            gc.collect()
            print("petla: " + str(gc.mem_free()))
            if hex(data[1]) == '0x11':
                if hex(data[2]) == '0x11':
                    frame_black = bytearray(bytes([255]) * fb_size)
                elif hex(data[2]) == '0x12':
                    frame_black = bytearray(bytes([0]) * fb_size)
            elif hex(data[1]) == '0x12':
                if hex(data[2]) == '0x11':
                    frame_red = bytearray(bytes([255]) * fb_size)
                elif hex(data[2]) == '0x12':
                    frame_red = bytearray(bytes([0]) * fb_size)

        # diplay color
        elif hex(data[0]) == '0xda':
            if hex(data[1]) == '0x11':
                e.Clear("white")
            elif hex(data[1]) == '0x12':
                e.Clear("black")
            elif hex(data[1]) == '0x13':
                e.Clear("red")
                
        # uploaded image display 
        elif hex(data[0]) == '0xdb':
            try:
                data = hex(data[0])[2:]  
                generated_screen(frame_black, frame_red, e, data.upper())
            except:
                pass
        
        # display update
        elif hex(data[0]) == '0xd1':
            e.display(frame_black, frame_red)

    # e.sleep()
    # deepsleep(1000*20*60) #20 minutes
    # deepsleep(2000)
