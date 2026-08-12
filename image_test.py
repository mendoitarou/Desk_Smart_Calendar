import sys
import os
import logging

import image_generate

try:
    logging.info("Generating the image...")
    image_generate.generate_image(True)
    logging.info("Success generate the image.")

except Exception as e:
    logging.info(e)
    print(e)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    exit()
