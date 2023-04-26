def is_noize_pixel(pixel) -> bool:
    return sum(pixel) / 3 < 20


def is_black_color(pixel) -> bool:
    return sum(pixel) / 3 < 100


def is_blue_pixel(pixel) -> bool:
    r, g, b = pixel
    return (r + g) / 2 < b
