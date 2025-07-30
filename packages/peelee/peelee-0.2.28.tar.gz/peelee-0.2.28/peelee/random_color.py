#!/usr/bin/env python3

from enum import Enum

from loguru import logger

from peelee import color_utils as CU
from peelee.color_utils import hex2hls, hex2rgb, hls2hex


class SliceType(Enum):
    """Color slice types"""

    DARKER = 0
    LIGHTER = 1


class SliceParameters(dict):
    """Slice parameters to generate slice colors"""

    def __init__(self, hex_color, n_slices, slice_type, **kwargs):
        self.hex_color = hex_color
        self.n_slices = n_slices
        self.slice_type = slice_type

        rgb_color = hex2rgb(hex_color)
        self.is_black_or_white_gray = max(rgb_color) == min(rgb_color)

        hls_color = hex2hls(self.hex_color)
        orig_hue = hls_color[0]
        orig_lightness = hls_color[1]
        orig_saturation = hls_color[2]
        self.hue = orig_hue
        self.lightness = orig_lightness
        self.saturation = orig_saturation
        # when generate slice colors used for background, saturation could be
        # True. however, keep mind that the generated color is not good to be
        # used as foreground color.
        self.keep_saturation = kwargs.get("keep_saturation", False)

        # max_lightness is used when generate lighter colors and it's used to
        # control the most light color would be
        # min_lightness is used when generate darker colors and it's used to
        # control the most dark color would be
        # both max_lightness and min_lightness should be a float value from 0
        # to 1
        self.max_lightness = kwargs.get(
            "max_lightness",
            1.0 if slice_type is SliceType.LIGHTER else self.lightness)
        self.min_lightness = kwargs.get(
            "min_lightness",
            self.lightness if slice_type is SliceType.LIGHTER else 0.0)

        self.max_saturation = kwargs.get("max_saturation", 1.0)
        self.min_saturation = kwargs.get("min_saturation", self.saturation)

        # calculate the int value of the lightness: convert lightness to int
        # value which will be used to generate slice steps
        self.lightness_decimal_length = max(len(str(self.lightness)[2:]), 16)
        self.int_full_lightness = 10**self.lightness_decimal_length
        self.int_lightness = int(self.lightness * self.int_full_lightness)

        self.int_max_lightness = int(self.max_lightness *
                                     10**self.lightness_decimal_length)
        self.int_min_lightness = int(self.min_lightness *
                                     10**self.lightness_decimal_length)

        # calculate the int value of the saturation
        self.saturation_decimal_length = max(len(str(self.saturation)[2:]), 16)
        self.int_full_saturation = 10**self.saturation_decimal_length
        self.int_saturation = int(self.saturation * self.int_full_saturation)

        # saturation range is stable no matter is to generate lighter or darker
        self.int_max_saturation = int(self.max_saturation *
                                      10**self.saturation_decimal_length)
        self.int_min_saturation = self.int_saturation

        # get slice steps of lightness and saturation
        self.lightness_slice_step: int = int(
            (self.int_max_lightness - self.int_min_lightness) // self.n_slices)
        self.saturation_slice_step: int = int(
            (self.int_max_saturation - self.int_min_saturation) //
            self.n_slices)

        super().update(
            hex_color=self.hex_color,
            hue=self.hue,
            lightness=self.lightness,
            saturation=self.saturation,
            n_slices=self.n_slices,
            slice_type=self.slice_type,
            is_black_or_white_gray=self.is_black_or_white_gray,
            min_lightness=self.min_lightness,
            max_lightness=self.max_lightness,
            min_saturation=self.min_saturation,
            max_saturation=self.max_saturation,
            int_lightness=self.int_lightness,
            int_saturation=self.int_saturation,
            int_max_lightness=self.int_max_lightness,
            int_min_lightness=self.int_min_lightness,
            int_max_saturation=self.int_max_saturation,
            int_min_saturation=self.int_min_saturation,
            int_full_lightness=self.int_full_lightness,
            int_full_saturation=self.int_full_saturation,
            lightness_slice_step=self.lightness_slice_step,
            saturation_slice_step=self.saturation_slice_step,
        )


def darker(base_color, n_color, **kwargs):
    """Given base color, return 'n' color hex codes from base color to darkest
    color."""
    return get_slice_colors(base_color, n_color, SliceType.DARKER, **kwargs)


def lighter(base_color, n_color, **kwargs):
    """Given base color, return 'n' color hex codes from base color to lightest
    color."""
    return get_slice_colors(base_color, n_color, SliceType.LIGHTER, **kwargs)


def get_slice_colors(hex_color,
                     n_slices,
                     color_slice_type: SliceType = SliceType.DARKER,
                     **kwargs):
    """Given base color, return 'n' color hex codes from base color to darkest
    color.

    Parameters:
        hex_color - base color in hex format.
        n_slices - how many slices to generate.
        color_slice_type - type of slice: DARKER or LIGHTER.

    Return:
        list - a list of hex colors generated by slicing the hex_color.
    """

    hue = kwargs.get("hue")
    saturation = kwargs.get("saturation")
    lightness = kwargs.get("lightness")
    hex_color = CU.set_hls_values(hex_color, hue, saturation, lightness)
    slice_parameters = SliceParameters(hex_color, n_slices, color_slice_type,
                                       **kwargs)

    lightness_list = get_lightness_list(slice_parameters)
    keep_saturation = slice_parameters.keep_saturation
    if keep_saturation:
        hex_slice_colors = [
            CU.set_lightness(hex_color,
                             lightness / slice_parameters.int_full_lightness)
            for lightness in lightness_list
        ]
    else:
        saturation_list = get_saturation_list(slice_parameters)

        hls_slice_colors = get_hls_slice_colors(slice_parameters,
                                                lightness_list,
                                                saturation_list)

        hex_slice_colors = [
            hls2hex(hls_color) for hls_color in hls_slice_colors
        ]
    if hex_color not in hex_slice_colors:
        if color_slice_type == SliceType.DARKER:
            hex_slice_colors = hex_slice_colors[0:-1]
            hex_slice_colors.append(hex_color)
        else:
            hex_slice_colors.insert(0, hex_color)
            hex_slice_colors = hex_slice_colors[0:-1]
    return hex_slice_colors


def get_lightness_list(slice_parameters: SliceParameters):
    """Generate a list of lightnesses based on slice parameters.

    Return:
        A list of lightness values.

    Refer to:
        class SliceParameters
    """
    n_slices = slice_parameters.n_slices
    int_min_lightness = slice_parameters.int_min_lightness
    int_max_lightness = slice_parameters.int_max_lightness
    color_slice_type = slice_parameters.slice_type
    lightness_slice_step = slice_parameters.lightness_slice_step

    if int_max_lightness == 0 and color_slice_type == SliceType.DARKER:
        lightness_list = [0 for _ in range(n_slices)]
    elif lightness_slice_step == 0:
        lightness_list = [int_min_lightness for _ in range(n_slices)]
    else:
        lightness_list = list(
            range(int_min_lightness, int_max_lightness,
                  lightness_slice_step)[0:n_slices])
    return lightness_list


def get_saturation_list(slice_parameters):
    """Generate a list of saturation based on slice parameters.

    Return:
        A list of lightness values.

    Refer to:
        class SliceParameters
    """
    n_slices = slice_parameters.n_slices
    slice_type = slice_parameters.slice_type
    is_black_or_white_gray = slice_parameters.is_black_or_white_gray
    int_saturation = slice_parameters.int_saturation
    int_max_saturation = slice_parameters.int_max_saturation
    int_min_saturation = slice_parameters.int_min_saturation
    saturation_slice_step = slice_parameters.saturation_slice_step

    # cannot be darker or won't change black to other color (e.g. red)
    if int_saturation == 0 and (slice_type == SliceType.DARKER
                                or is_black_or_white_gray):
        saturation_list = [0 for _ in range(n_slices)]
    elif int_saturation >= int_max_saturation and (
            slice_type == SliceType.LIGHTER or is_black_or_white_gray):
        saturation_list = [int_max_saturation for _ in range(n_slices)]
    elif saturation_slice_step == 0:
        saturation_list = [int_saturation for _ in range(n_slices)]
    elif slice_parameters.keep_saturation:
        saturation_list = [
            slice_parameters.saturation for _ in range(n_slices)
        ]
    else:
        try:
            saturation_list = list(
                range(int_min_saturation, int_max_saturation,
                      saturation_slice_step)[0:n_slices])
            if len(saturation_list) < n_slices:
                saturation_list = saturation_list + [int_max_saturation for _ in\
                                                     range(n_slices - len(saturation_list))]
        except ValueError as exc:
            logger.error(slice_parameters)
            raise exc
    return saturation_list


def get_hls_slice_colors(slice_parameters: SliceParameters, lightness_list,
                         saturation_list):
    """Generate HLS Slice Colors"""
    hue = slice_parameters.hue
    n_slices = slice_parameters.n_slices
    int_full_lightness = slice_parameters.int_full_lightness
    int_full_saturation = slice_parameters.int_full_saturation
    try:
        hls_slice_colors = [(
            hue,
            lightness_list[index] / int_full_lightness,
            saturation_list[index] / int_full_saturation,
        ) for index in range(n_slices)]
        return hls_slice_colors
    except IndexError as exc:
        logger.error((slice_parameters, lightness_list, saturation_list))
        raise exc
