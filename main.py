# imports from system libraries
from machine import Pin, SPI, deepsleep
from network import LoRa
import ubinascii
import socket
import pycom
import time

# imports from user files 
from pre_defined_displays import *
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

# create LoRa object
lora = LoRa(mode=LoRa.LORAWAN)
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create e-paper object and inicialize
e = epaper7in5b_HD.EPD(spi, cs, dc, rst, busy)

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D549915AE2B8')
app_key = ubinascii.unhexlify('F2C715A50B51C0ADBC4C7CD6675773F5')

while(True):
    # join a network using OTAA (Over the Air Activation)
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

    # wait until the module has joined the network
    join_time = 0
    while join_time != 16 and not lora.has_joined():
        time.sleep(2)
        join_time += 2
        print('Not yet joined...')

    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    # make the socket blocking
    s.setblocking(True)

    time.sleep(8)
    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    data = b'\xCB'
    if data != 0:
        e.init()
        fb_size = int(e.width * e.height)
        frame_black = bytearray(fb_size)
        frame_red = bytearray(fb_size)

        if data == b'\xAA':
            template(frame_black, frame_red, e)
            first_screen(frame_black, frame_red, e)
        elif data == b'\xAB':
            template(frame_black, frame_red, e)
            first_screen(frame_black, frame_red, e)
            brb(frame_black, frame_red, e)
        elif data == b'\xBA':
            second_screen(frame_black, frame_red, e)
        elif data == b'\xCA':
            template(frame_black, frame_red, e)
            third_screen(frame_black, frame_red, e)
        elif data == b'\xCB':
            template(frame_black, frame_red, e)
            third_screen(frame_black, frame_red, e)
            brb(frame_black, frame_red, e)

        e.display(frame_black, frame_red)

    
    e.sleep()
    deepsleep(1000*20*60) #20 minutes