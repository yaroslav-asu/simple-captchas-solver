from PIL import Image

from funcs import is_blue_pixel


class Img:
    def __init__(self, path):
        self.image = Image.open(path)
        self.size = self.image.size
        self.pixdata = self.image.load()

    def __del__(self):
        self.image.close()


class Captcha(Img):
    def __init__(self, reference_dir: str, title: str):
        super().__init__(f"{reference_dir}/{title}.png")
        self.title = title
        self.reference = Img(f"{reference_dir}/{title}.png")
        self.color = self.__color()

    def __color(self) -> str:
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if is_blue_pixel(self.pixdata[x, y]):
                    return "blue"
        return "black"

    def save(self, path: str):
        self.image.save(path)
