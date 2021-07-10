import sys
import digitalio
import busio
import board
import requests
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from PIL import Image, ImageDraw, ImageFont

api_url = 'http://pixel-shelf.local:3000'

# Cache
cached_count = None

def drawPixel(draw, x, y):
    draw.rectangle((x, y, x, y), fill=(0, 0, 0))

def drawAlien(draw, x, y):
    drawPixel(draw, 3 + x, 0 + y)
    drawPixel(draw, 8 + x, 0 + y)
    drawPixel(draw, 4 + x, 1 + y)
    drawPixel(draw, 7 + x, 1 + y)
    drawPixel(draw, 3 + x, 2 + y)
    drawPixel(draw, 4 + x, 2 + y)
    drawPixel(draw, 5 + x, 2 + y)
    drawPixel(draw, 6 + x, 2 + y)
    drawPixel(draw, 7 + x, 2 + y)
    drawPixel(draw, 8 + x, 2 + y)
    drawPixel(draw, 2 + x, 3 + y)
    drawPixel(draw, 3 + x, 3 + y)
    drawPixel(draw, 4 + x, 3 + y)
    drawPixel(draw, 5 + x, 3 + y)
    drawPixel(draw, 6 + x, 3 + y)
    drawPixel(draw, 7 + x, 3 + y)
    drawPixel(draw, 8 + x, 3 + y)
    drawPixel(draw, 9 + x, 3 + y)
    drawPixel(draw, 0 + x, 4 + y)
    drawPixel(draw, 2 + x, 4 + y)
    drawPixel(draw, 3 + x, 4 + y)
    drawPixel(draw, 5 + x, 4 + y)
    drawPixel(draw, 6 + x, 4 + y)
    drawPixel(draw, 8 + x, 4 + y)
    drawPixel(draw, 9 + x, 4 + y)
    drawPixel(draw, 11 + x, 4 + y)
    drawPixel(draw, 0 + x, 5 + y)
    drawPixel(draw, 2 + x, 5 + y)
    drawPixel(draw, 3 + x, 5 + y)
    drawPixel(draw, 5 + x, 5 + y)
    drawPixel(draw, 6 + x, 5 + y)
    drawPixel(draw, 8 + x, 5 + y)
    drawPixel(draw, 9 + x, 5 + y)
    drawPixel(draw, 11 + x, 5 + y)
    drawPixel(draw, 0 + x, 6 + y)
    drawPixel(draw, 1 + x, 6 + y)
    drawPixel(draw, 2 + x, 6 + y)
    drawPixel(draw, 3 + x, 6 + y)
    drawPixel(draw, 4 + x, 6 + y)
    drawPixel(draw, 5 + x, 6 + y)
    drawPixel(draw, 6 + x, 6 + y)
    drawPixel(draw, 7 + x, 6 + y)
    drawPixel(draw, 8 + x, 6 + y)
    drawPixel(draw, 9 + x, 6 + y)
    drawPixel(draw, 10 + x, 6 + y)
    drawPixel(draw, 11 + x, 6 + y)
    drawPixel(draw, 2 + x, 7 + y)
    drawPixel(draw, 3 + x, 7 + y)
    drawPixel(draw, 4 + x, 7 + y)
    drawPixel(draw, 5 + x, 7 + y)
    drawPixel(draw, 6 + x, 7 + y)
    drawPixel(draw, 7 + x, 7 + y)
    drawPixel(draw, 8 + x, 7 + y)
    drawPixel(draw, 9 + x, 7 + y)
    drawPixel(draw, 2 + x, 8 + y)
    drawPixel(draw, 3 + x, 8 + y)
    drawPixel(draw, 4 + x, 8 + y)
    drawPixel(draw, 5 + x, 8 + y)
    drawPixel(draw, 6 + x, 8 + y)
    drawPixel(draw, 7 + x, 8 + y)
    drawPixel(draw, 8 + x, 8 + y)
    drawPixel(draw, 9 + x, 8 + y)
    drawPixel(draw, 4 + x, 9 + y)
    drawPixel(draw, 7 + x, 9 + y)
    drawPixel(draw, 2 + x, 10 + y)
    drawPixel(draw, 3 + x, 10 + y)
    drawPixel(draw, 8 + x, 10 + y)
    drawPixel(draw, 9 + x, 10 + y)

def drawWatermark(draw, x, y):
    drawAlien(draw, x, y)
    draw.text((x + 15, y - 2), 'Powered by Pixel Shelf', font=small_font, fill=BLACK,)

def drawLibrarySize(draw, count):
    draw.text((5, 5), 'My Game Collection', font=medium_font, fill=BLACK,)
    draw.text((5, 25), str(count) + ' Games',font=large_font,fill=BLACK,)
    drawWatermark(draw, 5, 110)

def getLibraryCount(draw):
    try:
        r = requests.get(url = api_url + '/api/library/size')
        data = r.json()
        count = data['size']
        cached_count = count
        print('Fetched ' + str(count) + ' games from server')
    except requests.exceptions.ConnectionError:
        print('Could not fetch size from server!')
        # TODO: Display warning indicator on screen
        if cached_count:
            print('Falling back to cached count of ' + str(cached_count))
            return cached_count
        else:
            return '?'
    return count

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

display = Adafruit_SSD1680(122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy, )

display.rotation = 1

display.fill(Adafruit_EPD.WHITE)
image = Image.new("RGB", (display.width, display.height), color=WHITE)
draw = ImageDraw.Draw(image)
count = getLibraryCount(draw)
drawLibrarySize(draw, count)
image = image.convert("1").convert("L")

display.image(image)
display.display()