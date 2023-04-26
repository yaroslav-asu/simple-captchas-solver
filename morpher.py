from PIL import Image

from captcha import Captcha, Img
from funcs import is_blue_pixel, is_noize_pixel, is_black_color


class CaptchaMorpher:
    def __init__(self, default_captcha_dir: str, captcha_title: str, new_captcha_dir: str):
        self._captcha = Captcha(default_captcha_dir, captcha_title)
        self._captcha_save_path = f"{new_captcha_dir}/{captcha_title}.png"

    def remove_background(self) -> Captcha:
        gradient = Img("blank_gradient.png")
        for y in range(gradient.size[1]):
            for x in range(gradient.size[0]):
                captcha_pixel = self._captcha.pixdata[x, y]
                gradient_pixel = gradient.pixdata[x, y]
                if sum(gradient_pixel) - sum(captcha_pixel) < 60:
                    self._captcha.pixdata[x, y] = (abs(gradient_pixel[0] - captcha_pixel[0] - 255),
                                                   abs(gradient_pixel[1] - captcha_pixel[1] - 255),
                                                   abs(gradient_pixel[2] - captcha_pixel[2] - 255))
        return self._captcha

    def remove_noize(self) -> Captcha:
        for y in range(self._captcha.size[1]):
            for x in range(self._captcha.size[0]):
                pixel = self._captcha.reference.pixdata[x, y]
                if sum(pixel) / 3 < 20:
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
                if self._captcha.color == "blue" and is_blue_pixel(pixel):
                    self._captcha.pixdata[x, y] = (0, 0, 0)
                elif self._captcha.color == "black" and not is_noize_pixel(pixel) and is_black_color(pixel):
                    self._captcha.pixdata[x, y] = (0, 0, 0)
        return self._captcha

    def save_captcha(self):
        self._captcha.save(self._captcha_save_path)


if __name__ == "__main__":
    morpher = CaptchaMorpher("captcha", "2ak2k", "new")
    # morpher.remove_noize()
    # morpher.remove_background()
    # morpher.make_captcha_font_black()
    morpher.save_captcha()
