default_new_save_path = "morphs/"

def is_deep_black(pixel) -> bool:
    return sum(pixel) / 3 < 20


def is_black_letter(pixel) -> bool:
    return not is_deep_black(pixel) and sum(pixel) / 3 < 160


def is_deep_blue(pixel):
    r, g, b = pixel
    return r + g < b


def is_blue_letter(pixel) -> bool:
    r, g, b = pixel
    return (r + g) / 2 < b
