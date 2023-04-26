from PIL import Image

from captcha import Captcha


class CaptchaMorpher:
    def __init__(self, default_captcha_dir: str, captcha_title: str, new_captcha_dir: str):
        self.captcha = Captcha(default_captcha_dir, captcha_title)
        self.captcha_save_path = f"{new_captcha_dir}/{captcha_title}.png"

    @staticmethod
    def remove_background(captcha: Captcha) -> Captcha:
        gradient = Image.open("blank_gradient.png")
        gradient_size = gradient.size
        gradient_pixdata = gradient.load()

        for y in range(gradient_size[1]):
            for x in range(gradient_size[0]):
                captcha_pixel = captcha.pixdata[x, y]
                gradient_pixel = gradient_pixdata[x, y]
                if sum(gradient_pixel) - sum(captcha_pixel) < 60:
                    captcha.pixdata[x, y] = (abs(gradient_pixel[0] - captcha_pixel[0] - 255),
                                             abs(gradient_pixel[1] - captcha_pixel[1] - 255),
                                             abs(gradient_pixel[2] - captcha_pixel[2] - 255))

        gradient.close()
        return captcha

    @staticmethod
    def remove_noize(captcha: Captcha) -> Captcha:
        for y in range(captcha.size[1]):
            for x in range(captcha.size[0]):
                pixel = captcha.reference.pixdata[x, y]
                if sum(pixel) / 3 < 20:
                    captcha.pixdata[x, y] = (255, 255, 255)
                    for i in [-1, 1]:
                        if 0 < x + i < captcha.size[0]:
                            captcha.pixdata[x + i, y] = (255, 255, 255)
                        if 0 < y + i < captcha.size[1]:
                            captcha.pixdata[x, y + i] = (255, 255, 255)
        return captcha
