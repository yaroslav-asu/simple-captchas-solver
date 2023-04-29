import os.path

import cv2
import typing

import numpy as np
from mltu.configs import BaseModelConfigs
from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder

from captcha import Captcha, Path
import sys

from utils import root_dir


class ImageToWordModel(OnnxInferenceModel):
    def __init__(self, char_list: typing.Union[str, list], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_list = char_list

    def predict(self, image: np.ndarray):
        image = cv2.resize(image, self.input_shape[:2][::-1])

        image_pred = np.expand_dims(image, axis=0).astype(np.float32)

        preds = self.model.run(None, {self.input_name: image_pred})[0]

        text = ctc_decoder(preds, self.char_list)[0]

        return text


class Solver:
    def __init__(self, captcha_path: str) -> None:
        self._captcha = Captcha(Path(captcha_path))
        configs = BaseModelConfigs.load(os.path.join(root_dir, "simple-captchas-solve-model/configs.yaml"))
        self._model = ImageToWordModel(model_path=os.path.join(root_dir, "simple-captchas-solve-model"),
                                       char_list=configs.vocab)

    def solve(self) -> str:
        self._captcha.morph()
        return self._model.predict(np.array(self._captcha.image))


if __name__ == "__main__":
    print(Solver(sys.argv[1]).solve())
