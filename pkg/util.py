"""Utility functions."""


def rgb_to_hex(r, g, b):
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)


def hex_to_rgb(hex):
    """
    Convert an RGB hex string to an HSV tuple.

    rgb -- RGB hex string, i.e. #123456

    Returns an RGB tuple, i.e. (360, 100, 100).
    """
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i + 2], 16) / 255 for i in range(0, 6, 2))


def byteToPercent(byte):
    if not byte:
        return 0

    if byte > 255:
        byte = 255
    if byte < 0:
        byte = 0
    return int((byte * 100)/255)


def percentToByte(percent):
    if not percent:
        return 0
    if percent > 100:
        percent = 100
    if percent < 0:
        percent = 0
    return int((percent * 255)/100)
