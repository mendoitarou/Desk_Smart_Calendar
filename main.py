#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

path = os.getcwd()

import logging
from lib.waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import image_generate

#logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V4 Demo")
    
    epd = epd2in13_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
    logging.info("E-paper refresh")
    epd.init()

    logging.info("Generating the image...")
    image = image_generate.generate_image()

    #logging.info("Drawing on the image...")
    #image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    #draw = ImageDraw.Draw(image)

    logging.info("read image...")
    #logging.info("read bmp file...")
    #image = Image.open('latest.bmp')
    image = image.rotate(180)
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    
    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except Exception as e:
    logging.info(e)
    text = f"\n[LOG][ERROR]MESSAGE: {e}\n"
    log_path = path+"/error_log.txt"
    with open(log_path, mode='a') as f:
        f.write(text)
    print(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
