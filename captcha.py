import os

from PIL import Image
from os import listdir
from os.path import join, isfile

from utils import is_blue_letter, is_black_letter, is_deep_black, is_deep_blue, root_dir


class Path:
    def __init__(self, full_path: str):
        self.full_path = full_path
        self.title = self.full_path.split("/")[-1]
        self.dir = "/".join(self.full_path.split("/")[:-1])


class Img:
    def __init__(self, path: str):
        self.image: Image = Image.open(path)
        self.size = self.image.size
        self.pixdata = self.image.load()

    def __del__(self):
        self.image.close()


class Captcha(Img):
    def __init__(self, path: Path) -> None:
        super().__init__(path.full_path)
        self.path = path
        self.reference = Img(path.full_path)
        self.color = self.__color()

    def __color(self) -> str:
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if is_blue_letter(self.pixdata[x, y]):
                    return "blue"
        return "black"

    def save(self, path: str) -> None:
        self.image.save(path + self.path.title)

    def morph(self) -> None:
        morpher = CaptchaMorpher(self)
        morpher.remove_background()
        morpher.make_captcha_font_black()


class CaptchaMorpher:
    def __init__(self, captcha: Captcha) -> None:
        self._captcha = captcha

    def remove_background(self) -> Image:
        gradient = Img(os.path.join(root_dir, "blank_gradient.png"))
        for y in range(gradient.size[1]):
            for x in range(gradient.size[0]):
                captcha_pixel = self._captcha.pixdata[x, y]
                gradient_pixel = gradient.pixdata[x, y]
                if not is_deep_blue(captcha_pixel) and sum(gradient_pixel) - sum(captcha_pixel) < 60:
                    self._captcha.pixdata[x, y] = tuple(
                        [abs(gradient_pixel[i] - captcha_pixel[i] - 255) for i in range(3)]
                    )
        return self._captcha.image

    def remove_noize(self) -> Image:
        for y in range(self._captcha.size[1]):
            for x in range(self._captcha.size[0]):
                pixel = self._captcha.reference.pixdata[x, y]
                if is_deep_black(pixel):
                    self._captcha.pixdata[x, y] = (255, 255, 255)
                    for i in [-1, 1]:
                        if 0 < x + i < self._captcha.size[0]:
                            self._captcha.pixdata[x + i, y] = (255, 255, 255)
                        if 0 < y + i < self._captcha.size[1]:
                            self._captcha.pixdata[x, y + i] = (255, 255, 255)
        return self._captcha.image

    def make_captcha_font_black(self) -> Image:
        for y in range(self._captcha.size[1]):
            for x in range(self._captcha.size[0]):
                pixel = self._captcha.pixdata[x, y]
                if self._captcha.color == "blue" and is_blue_letter(pixel):
                    self._captcha.pixdata[x, y] = (0, 0, 0)
                elif self._captcha.color == "black" and is_black_letter(pixel):
                    self._captcha.pixdata[x, y] = (0, 0, 0)
        return self._captcha.image


def morph_all_capthas(captchas_dir: str, save_dir: str) -> None:
    for file in [f for f in listdir(captchas_dir) if isfile(join(captchas_dir, f))]:
        captcha = Captcha(Path(captchas_dir + file))
        captcha.morph()
        captcha.save(save_dir)


if __name__ == "__main__":
    captchas_dir = "./reference/"
    save_dir = "./morphs/"
    morph_all_capthas(captchas_dir, save_dir)
