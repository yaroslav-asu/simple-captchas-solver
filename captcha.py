from PIL import Image
from os import listdir
from os.path import join, isfile

import utils
from utils import is_blue_letter, is_black_letter, is_deep_black, is_deep_blue


class Path:
    def __init__(self, full_path: str):
        self.full_path = full_path
        self.title = self.full_path.split("/")[-1]
        self.dir = "/".join(self.full_path.split("/")[:-1])


class Img:
    def __init__(self, path: str):
        self.image = Image.open(path)
        self.size = self.image.size
        self.pixdata = self.image.load()

    def __del__(self):
        self.image.close()


class Captcha(Img):
    def __init__(self, path: Path):
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

    def save(self, path: str):
        self.image.save(path)

    def morph(self, save_dir: str) -> None:
        morpher = CaptchaMorpher(self.path, save_dir)
        morpher.remove_background()
        morpher.make_captcha_font_black()
        morpher.save_captcha()


class CaptchaMorpher:
    def __init__(self, captcha_path: Path, new_captcha_dir: str):
        self._captcha = Captcha(captcha_path)
        self._captcha_save_path = new_captcha_dir

    def remove_background(self) -> Captcha:
        gradient = Img("blank_gradient.png")
        for y in range(gradient.size[1]):
            for x in range(gradient.size[0]):
                captcha_pixel = self._captcha.pixdata[x, y]
                gradient_pixel = gradient.pixdata[x, y]
                if not is_deep_blue(captcha_pixel) and sum(gradient_pixel) - sum(captcha_pixel) < 60:
                    self._captcha.pixdata[x, y] = tuple(
                        [abs(gradient_pixel[i] - captcha_pixel[i] - 255) for i in range(3)]
                    )
        return self._captcha

    def remove_noize(self) -> Captcha:
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
        return self._captcha

    def make_captcha_font_black(self) -> Captcha:
        for y in range(self._captcha.size[1]):
            for x in range(self._captcha.size[0]):
                pixel = self._captcha.pixdata[x, y]
                if self._captcha.color == "blue" and is_blue_letter(pixel):
                    self._captcha.pixdata[x, y] = (0, 0, 0)
                elif self._captcha.color == "black" and is_black_letter(pixel):
                    self._captcha.pixdata[x, y] = (0, 0, 0)
        return self._captcha

    def save_captcha(self):
        self._captcha.save(self._captcha_save_path + self._captcha.path.title)


def morph_all_capthas(captchas_dir: str, save_dir: str) -> None:
    for file in [f for f in listdir(captchas_dir) if isfile(join(captchas_dir, f))]:
        captcha = Captcha(Path(captchas_dir + file))
        captcha.morph(save_dir)


if __name__ == "__main__":
    captchas_dir = "./reference/"
    save_dir = utils.default_new_save_path
    morph_all_capthas(captchas_dir, save_dir)
