import logging, re
import pyzbar.pyzbar as pyzbar
from PIL import Image

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
