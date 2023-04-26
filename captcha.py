from PIL import Image


def is_black_pixel(r, g, b):
    return (r + g + b) / 3 < 20


def is_blue_pixel(r, g, b):
    return (r + g) / 2 < b


class Captcha:
    def __init__(self, original_path):
        self.reference = Image.open(original_path)
        self.size = self.reference.size
        self.pixdata = self.reference.load()

    def __del__(self):
        self.reference.close()

    def color(self) -> str:
        for y in range(self.image_size[1]):
            for x in range(self.image_size[0]):
                if is_blue_pixel(*self.pixdata[x, y]):
                    return "blue"
        return "black"

