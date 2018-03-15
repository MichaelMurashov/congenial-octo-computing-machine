import logging, re
import pyzbar.pyzbar as pyzbar
from PIL import Image, ImageFilter, ImageDraw

logger = logging.getLogger(__name__)


class Data:
    def __init__(self, _fn, _fp, _i):
        self.fss = _fn
        self.tickets = _i
        self.facial_sign = _fp


def parse_data(data):
    result = re.split(r'&', data)

    fn = re.split(r'=', result[2])[1]
    fp = re.split(r'=', result[4])[1]
    i = re.split(r'=', result[3])[1]

    if fn != '' and fp != '' and i != '':
        return Data(fn, fp, i)
    else:
        return None


def decode(file_path):
    image = Image.open(file_path)
    decoded_objects = pyzbar.decode(image)

    if len(decoded_objects) != 0:
        return parse_data(decoded_objects[0].data.decode())
    else:
        return None


def decode_with_img_proc(file_path):
    image = Image.open(file_path)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    draw = ImageDraw.Draw(image)

    # Перевод в чб
    factor = 0
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = a + b + c
            if (S > (((255 + factor) // 2) * 3)):
                a, b, c = 255, 255, 255
            else:
                a, b, c = 0, 0, 0

            draw.point((i, j), (a, b, c))

    # Морфологическое сужение
    image = image.filter(ImageFilter.MinFilter)
    # Морфологическое расширение
    image = image.filter(ImageFilter.MaxFilter)

    image.save(file_path, 'JPEG')

    decoded_objects = pyzbar.decode(image)
    if len(decoded_objects) != 0:
        return parse_data(decoded_objects[0].data.decode())
    else:
        return None
