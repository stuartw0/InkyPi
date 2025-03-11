from plugins.base_plugin.base_plugin import BasePlugin
from utils.app_utils import get_font
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import logging
import random

logger = logging.getLogger(__name__)

class Christmas(BasePlugin):
    def generate_image(self, settings, device_config):
        text_color = "black"

        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        img_index = settings.get("image_index", 0)
        image_locations = settings.get("imageFiles[]")

        randomise = settings.get('randomiseImage') == 'true'

        if img_index >= len(image_locations):
            # reset if image_locations changed
            img_index = 0

        if not image_locations:
            raise RuntimeError("No images provided.")
        # Open the image using Pillow
        
        try:
            baseimage = Image.open(image_locations[img_index])
        except Exception as e:
            logger.error(f"Failed to read image file: {str(e)}")
            raise RuntimeError("Failed to read image file.")

        # Get days until Christmas and generate banner text
        try:
            days = Christmas.count_days()
            image = Christmas.text_banner(baseimage, days)
        except Exception as e:
            logger.error(f"Failed to generate banner text {str(e)}")
            raise RuntimeError("Text banner failure, please check logs.")

        if randomise:
            settings['image_index'] = (random.randint(0, len(image_locations)))
        else:
            settings['image_index'] = (img_index + 1) % len(image_locations)

        return image

    @staticmethod
    def text_banner(image, text):
        w,h = image.size
        dim = min(w,h)
        width = max(int(dim*0.103), 7)
        padding = max(dim*0.05, 1)
        text_font_size = int(dim*0.088)
        text_font = get_font("Jost", text_font_size, font_weight="bold")
        #text_font = get_font("jost-semibold", text_font_size)
        y = h-(2*padding)
        x = w/2

        image_draw = ImageDraw.Draw(image)
        image_draw.line([ ((2*padding), h-(2*padding)), (w-(2*padding), h-(2*padding))], fill="white", width=width)
        image_draw.text((x, y), text, anchor="mm", fill="black", font=text_font)

        return image

    @staticmethod
    def count_days():
        dt = datetime
        now = datetime.now()
        eventName = "Christmas"
        days_until = datetime(year = 2025, month = 12, day = 25) - datetime(year=now.year, month=now.month, day=now.day)
        if(days_until.days<0):
            days_left = "{} has already passed!".format(eventName)
        elif(days_until.days==0):
            days_left = "Merry Christmas!"
        elif(days_until.days==1):
            days_left = "It's {} day until {}!".format(days_until.days, eventName)
        else:
            days_left = "It's {} days until {}!".format(days_until.days, eventName)
        return days_left
