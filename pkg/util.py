"""Utility functions."""

import colorsys


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
