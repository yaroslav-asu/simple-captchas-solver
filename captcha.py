from PIL import Image


def is_black_pixel(r, g, b):
    return (r + g + b) / 3 < 20


def is_blue_pixel(r, g, b):
    return (r + g) / 2 < b


class CaptchaImage:
    def __init__(self, path):
        self.image = Image.open(path)
        self.size = self.image.size
        self.pixdata = self.image.load()

    def __del__(self):
        self.image.close()


class Captcha(CaptchaImage):
    def __init__(self, reference_dir: str, title: str):
        super().__init__(f"{reference_dir}/{title}.png")
        self.title = title
        self.reference = CaptchaImage(f"{reference_dir}/{title}.png")

    def color(self) -> str:
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if is_blue_pixel(*self.pixdata[x, y]):
                    return "blue"
        return "black"

    def save(self, path: str):
        self.image.save(path)