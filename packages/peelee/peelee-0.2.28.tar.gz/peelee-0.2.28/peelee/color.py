#!/usr/bin/env python3
"""
Utilities
"""
import re
from enum import Enum

from loguru import logger

from peelee import color_utils as CU
from peelee import random_color as R

HLS_MAX = 10**16
SLICE_COLORS_TOTAL = 100


class ColorName(Enum):
    """Color names"""

    WHITE = "WH"
    GRAY = "AY"
    RED = "RE"
    GREEN = "GR"
    BLUE = "BL"
    YELLOW = "YE"
    CYAN = "CY"
    VIOLET = "VI"
    OBSIDIAN = "OB"  # Obsidian
    RANDOM = "RA"


def get_color_name(hex_code):
    """Check the value of ColorName for the given hex code."""
    h, _, _ = CU.hex2hls(hex_code)


class ColorHex(Enum):
    """Color codes for 16 bit color mode"""

    FG_BLACK = "#000000"
    FG_RED = "#FF0000"
    FG_GREEN = "#00FF00"
    FG_YELLOW = "#FFFF00"
    FG_BLUE = "#0000FF"
    FG_MAGENTA = "#FF00FF"
    FG_CYAN = "#00FFFF"
    FG_WHITE = "#FFFFFF"
    FG_BRIGT_BLACK = "#808080"
    FG_BRIGHT_RED = "#FF8080"
    FG_BRIGHT_GREEN = "#80FF80"
    FG_BRIGHT_YELLOW = "#FFFF80"
    FG_BRIGHT_BLUE = "#8080FF"
    FG_BRIGHT_MAGENTA = "#FF80FF"
    FG_BRIGHT_CYAN = "#80FFFF"
    FG_BRIGHT_WHITE = "#FFFFFF"
    BG_BLACK = "#000000"
    BG_RED = "#800000"
    BG_GREEN = "#008000"


class Color4Bit(Enum):
    """Color codes for 4 bit color mode"""

    FG_BLACK = 30
    FG_RED = 31
    FG_GREEN = 32
    FG_YELLOW = 33
    FG_BLUE = 34
    FG_MAGENTA = 35
    FG_CYAN = 36
    FG_WHITE = 37
    FG_BRIGT_BLACK = 90
    FG_BRIGHT_RED = 91
    FG_BRIGHT_GREEN = 92
    FG_BRIGHT_YELLOW = 93
    FG_BRIGHT_BLUE = 94
    FG_BRIGHT_MAGENTA = 95
    FG_BRIGHT_CYAN = 96
    FG_BRIGHT_WHITE = 97
    BG_BLACK = 40
    BG_RED = 41
    BG_GREEN = 42
    BG_YELLOW = 43
    BG_BLUE = 44
    BG_MAGENTA = 45
    BG_CYAN = 46
    BG_WHITE = 47
    BG_BRIGT_BLACK = 100
    BG_BRIGHT_RED = 101
    BG_BRIGHT_GREEN = 102
    BG_BRIGHT_YELLOW = 103
    BG_BRIGHT_BLUE = 104
    BG_BRIGHT_MAGENTA = 105
    BG_BRIGHT_CYAN = 106
    BG_BRIGHT_WHITE = 107


class StandardColor(Enum):
    """Standard colors"""

    OBSIDIAN = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    LIGHT_GRAY = 7


class HighIntensityColor(Enum):
    """High intensity colors"""

    DARK_GRAY = 8
    BRIGHT_RED = 9
    BRIGHT_GREEN = 10
    BRIGHT_YELLOW = 11
    BRIGHT_BLUE = 12
    BRIGHT_MAGENTA = 13
    BRIGHT_CYAN = 14
    WHITE = 15


COLOR_8BIT_GRAY_COLORS = [code for code in range(232, 256)]
COLOR_8BIT_HEX_CODE_LIST = [
    "#000000",
    "#000080",
    "#008000",
    "#008080",
    "#800000",
    "#800080",
    "#808000",
    "#C0C0C0",
    "#808080",
    "#0000FF",
    "#00FF00",
    "#00FFFF",
    "#FF0000",
    "#FF00FF",
    "#FFFF00",
    "#FFFFFF",
    "#000000",
    "#00005F",
    "#000087",
    "#0000AF",
    "#0000D7",
    "#0000FF",
    "#005F00",
    "#005F5F",
    "#005F87",
    "#005FAF",
    "#005FD7",
    "#005FFF",
    "#008700",
    "#00875F",
    "#008787",
    "#0087AF",
    "#0087D7",
    "#0087FF",
    "#00AF00",
    "#00AF5F",
    "#00AF87",
    "#00AFAF",
    "#00AFD7",
    "#00AFFF",
    "#00D700",
    "#00D75F",
    "#00D787",
    "#00D7AF",
    "#00D7D7",
    "#00D7FF",
    "#00FF00",
    "#00FF5F",
    "#00FF87",
    "#00FFAF",
    "#00FFD7",
    "#00FFFF",
    "#5F0000",
    "#5F005F",
    "#5F0087",
    "#5F00AF",
    "#5F00D7",
    "#5F00FF",
    "#5F5F00",
    "#5F5F5F",
    "#5F5F87",
    "#5F5FAF",
    "#5F5FD7",
    "#5F5FFF",
    "#5F8700",
    "#5F875F",
    "#5F8787",
    "#5F87AF",
    "#5F87D7",
    "#5F87FF",
    "#5FAF00",
    "#5FAF5F",
    "#5FAF87",
    "#5FAFAF",
    "#5FAFD7",
    "#5FAFFF",
    "#5FD700",
    "#5FD75F",
    "#5FD787",
    "#5FD7AF",
    "#5FD7D7",
    "#5FD7FF",
    "#5FFF00",
    "#5FFF5F",
    "#5FFF87",
    "#5FFFAF",
    "#5FFFD7",
    "#5FFFFF",
    "#870000",
    "#87005F",
    "#870087",
    "#8700AF",
    "#8700D7",
    "#8700FF",
    "#875F00",
    "#875F5F",
    "#875F87",
    "#875FAF",
    "#875FD7",
    "#875FFF",
    "#878700",
    "#87875F",
    "#878787",
    "#8787AF",
    "#8787D7",
    "#8787FF",
    "#87AF00",
    "#87AF5F",
    "#87AF87",
    "#87AFAF",
    "#87AFD7",
    "#87AFFF",
    "#87D700",
    "#87D75F",
    "#87D787",
    "#87D7AF",
    "#87D7D7",
    "#87D7FF",
    "#87FF00",
    "#87FF5F",
    "#87FF87",
    "#87FFAF",
    "#87FFD7",
    "#87FFFF",
    "#AF0000",
    "#AF005F",
    "#AF0087",
    "#AF00AF",
    "#AF00D7",
    "#AF00FF",
    "#AF5F00",
    "#AF5F5F",
    "#AF5F87",
    "#AF5FAF",
    "#AF5FD7",
    "#AF5FFF",
    "#AF8700",
    "#AF875F",
    "#AF8787",
    "#AF87AF",
    "#AF87D7",
    "#AF87FF",
    "#AFAF00",
    "#AFAF5F",
    "#AFAF87",
    "#AFAFAF",
    "#AFAFD7",
    "#AFAFFF",
    "#AFD700",
    "#AFD75F",
    "#AFD787",
    "#AFD7AF",
    "#AFD7D7",
    "#AFD7FF",
    "#AFFF00",
    "#AFFF5F",
    "#AFFF87",
    "#AFFFAF",
    "#AFFFD7",
    "#AFFFFF",
    "#D70000",
    "#D7005F",
    "#D70087",
    "#D700AF",
    "#D700D7",
    "#D700FF",
    "#D75F00",
    "#D75F5F",
    "#D75F87",
    "#D75FAF",
    "#D75FD7",
    "#D75FFF",
    "#D78700",
    "#D7875F",
    "#D78787",
    "#D787AF",
    "#D787D7",
    "#D787FF",
    "#D7AF00",
    "#D7AF5F",
    "#D7AF87",
    "#D7AFAF",
    "#D7AFD7",
    "#D7AFFF",
    "#D7D700",
    "#D7D75F",
    "#D7D787",
    "#D7D7AF",
    "#D7D7D7",
    "#D7D7FF",
    "#D7FF00",
    "#D7FF5F",
    "#D7FF87",
    "#D7FFAF",
    "#D7FFD7",
    "#D7FFFF",
    "#FF0000",
    "#FF005F",
    "#FF0087",
    "#FF00AF",
    "#FF00D7",
    "#FF00FF",
    "#FF5F00",
    "#FF5F5F",
    "#FF5F87",
    "#FF5FAF",
    "#FF5FD7",
    "#FF5FFF",
    "#FF8700",
    "#FF875F",
    "#FF8787",
    "#FF87AF",
    "#FF87D7",
    "#FF87FF",
    "#FFAF00",
    "#FFAF5F",
    "#FFAF87",
    "#FFAFAF",
    "#FFAFD7",
    "#FFAFFF",
    "#FFD700",
    "#FFD75F",
    "#FFD787",
    "#FFD7AF",
    "#FFD7D7",
    "#FFD7FF",
    "#FFFF00",
    "#FFFF5F",
    "#FFFF87",
    "#FFFFAF",
    "#FFFFD7",
    "#FFFFFF",
    "#080808",
    "#121212",
    "#1C1C1C",
    "#262626",
    "#303030",
    "#3A3A3A",
    "#444444",
    "#4E4E4E",
    "#585858",
    "#626262",
    "#6C6C6C",
    "#767676",
    "#808080",
    "#8A8A8A",
    "#949494",
    "#9E9E9E",
    "#A8A8A8",
    "#B2B2B2",
    "#BCBCBC",
    "#C6C6C6",
    "#D0D0D0",
    "#DADADA",
    "#E4E4E4",
    "#EEEEEE",
]


def crange(s, t, total):
    if s == t:
        return [s * HLS_MAX] * total
    _start = min(s, t)
    _end = max(s, t)
    _step = (_end - _start) / total
    _list = list(
        range(
            round(_start * HLS_MAX),
            round(_end * HLS_MAX),
            round(_step * HLS_MAX),
        )
    )
    if s not in _list:
        _list.insert(0, s * HLS_MAX)
    if t not in _list:
        _list.append(t * HLS_MAX)
    return _list


def generate_gradient_colors(hex_color_source, hex_color_target, total):
    """Generate gradient colors.

    Parameters:
        hex_color_source - hex color code of the source color
        hex_color_target - hex color code of the target color
        total - total number of colors

    Returns:
        list
    """
    h, l, s = CU.hex2hls(hex_color_source)
    h_target, l_target, s_target = CU.hex2hls(hex_color_target)
    h_list = crange(h, h_target, total)
    l_list = crange(l, l_target, total)
    s_list = crange(s, s_target, total)

    hls_list = [
        (
            h_list[index] / HLS_MAX,
            l_list[index] / HLS_MAX,
            s_list[index] / HLS_MAX,
        )
        for index in range(total)
    ]
    gradient_colors = [CU.hls2hex(hls) for hls in hls_list]
    if hex_color_source not in gradient_colors:
        gradient_colors.insert(0, hex_color_source)
    if hex_color_target not in gradient_colors:
        gradient_colors.append(hex_color_target)
    return gradient_colors


def calculate_relative_luminance(hex_color):
    """Calculate relative luminance for hex color codes.

    Refer to:
    https://www.w3.org/TR/WCAG20-TECHS/G17.html

    Parameter:
    hex_color - hex color code
    """
    rgb_8bit = CU.hex2rgb(hex_color)
    rgb_srgb = tuple(_8bit / 255.0 for _8bit in rgb_8bit)
    r, g, b = tuple(
        _srgb / 12.92 if _srgb <= 0.03928 else ((_srgb + 0.055) / 1.055) ** 2.4
        for _srgb in rgb_srgb
    )

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def calculate_contrast_ratio(hex_light_color, hex_dark_color):
    """Calculate contrast ratio for hex color codes.

    Parameter:
    hex_light_color - hex color code of the lighter of the foreground or background color
    hex_dark_color - hex color code of the darker of the foreground or background color

    Refer to:
    https://www.w3.org/TR/WCAG20-TECHS/G17.html
    """
    relative_luminance_light = calculate_relative_luminance(hex_light_color)
    relative_luminance_dark = calculate_relative_luminance(hex_dark_color)
    return (relative_luminance_light + 0.05) / (relative_luminance_dark + 0.05)


def convert_to_best_light_color(
    base_light_color,
    target_dark_color="#000000",
    min_contrast_ratio=10,
    max_contrast_ratio=21,
    choose_lightest=False,
):
    """Converts the given base light color to the best light color.

    This function converts the given base light color to the best light color based on contrast ratio.

    Parameters:
        base_light_color (str): The base light color.
        target_background_color (str): The target background color.
    """
    best_color = base_light_color
    contrast_ratio = calculate_contrast_ratio(base_light_color, target_dark_color)
    # already good enough contrast ratio, return directly
    if contrast_ratio >= min_contrast_ratio and contrast_ratio <= max_contrast_ratio:
        return best_color

    # if too light, choose the darkest light color; if too dark, choose the
    # lightest light color
    is_too_light = contrast_ratio > max_contrast_ratio
    is_too_dark = contrast_ratio < min_contrast_ratio
    better_colors = []
    if is_too_dark:
        better_colors = R.lighter(base_light_color, SLICE_COLORS_TOTAL)
    elif is_too_light:
        better_colors = R.darker(base_light_color, SLICE_COLORS_TOTAL)

    filter_better_colors = list(
        filter(
            lambda x: calculate_contrast_ratio(x, target_dark_color)
            >= min_contrast_ratio
            and calculate_contrast_ratio(x, target_dark_color) <= max_contrast_ratio,
            better_colors,
        )
    )
    # choose the darkest light color which has lowest contrast ratio
    # to make sure it's not too light
    if len(filter_better_colors) == 0:
        logger.warning(
            f"Not found best light color for {base_light_color} to adapt to the dark color: {target_dark_color}"
        )
        logger.warning(
            (
                base_light_color,
                target_dark_color,
                better_colors[0],
                better_colors[-1],
                min_contrast_ratio,
                max_contrast_ratio,
                calculate_contrast_ratio(better_colors[0], target_dark_color),
                calculate_contrast_ratio(better_colors[-1], target_dark_color),
                filter_better_colors,
            )
        )
        # for some colors, could not be even better (the pre-defined contrast
        # ratio is unrealistic), so just use the better colors
        filter_better_colors = better_colors
    # the darkest light color is the best light color
    # this is the proved best light color, don't make change to it
    _index = 0 if not choose_lightest else -1
    best_color = sorted(filter_better_colors)[_index]
    return best_color


def convert_to_best_dark_color(
    base_dark_color,
    target_light_color="#FFFFFF",
    min_contrast_ratio=10,
    max_contrast_ratio=21,
    choose_darkest=False,
):
    """Converts the given base light color to the best light color.

    This function converts the given base light color to the best light color based on contrast ratio.

    Parameters:
        base_light_color (str): The base light color.
        target_background_color (str): The target background color.
    """
    best_color = base_dark_color
    contrast_ratio = calculate_contrast_ratio(target_light_color, base_dark_color)
    if contrast_ratio >= min_contrast_ratio and contrast_ratio <= max_contrast_ratio:
        return best_color

    # if too dark, choose the lightest dark color; if too light, choose the
    # darkest dark color
    better_colors = []
    if contrast_ratio < min_contrast_ratio:
        better_colors = R.darker(base_dark_color, SLICE_COLORS_TOTAL)
    elif contrast_ratio > max_contrast_ratio:
        better_colors = R.lighter(base_dark_color, SLICE_COLORS_TOTAL)
    filter_better_colors = list(
        filter(
            lambda x: calculate_contrast_ratio(target_light_color, x)
            >= min_contrast_ratio
            and calculate_contrast_ratio(target_light_color, x) <= max_contrast_ratio,
            better_colors,
        )
    )
    # choose the lightest dark color which has lowest contrast ratio
    # to make sure it's not too dark
    if len(filter_better_colors) == 0:
        logger.warning(
            (
                base_dark_color,
                target_light_color,
                better_colors[0],
                better_colors[-1],
                min_contrast_ratio,
                max_contrast_ratio,
                calculate_contrast_ratio(target_light_color, better_colors[0]),
                calculate_contrast_ratio(target_light_color, better_colors[-1]),
                filter_better_colors,
            )
        )
        logger.warning(
            f"Not found best dark color for {base_dark_color} to adapt to the light color: {target_light_color}"
        )
        return best_color
    # the lightest dark color is the best one
    # this is the proved best dark color, don't make change to it
    # unless it's to find the best editor background color
    if choose_darkest:
        best_color = sorted(filter_better_colors)[0]
    else:
        best_color = sorted(filter_better_colors)[-1]
    return best_color


def find_the_cloest_color(hex_color, hex_color_list):
    """Find the clost color in the hex_color_list for the given hex_color.

    NOTE: it's not reliable to get the cloest color for human eyes yet.
    Parameters
    ----------
    hex_color: str
        hex color code such as "#565656"
    hex_color_list: typing.List[str]
        hex color code list from which to find the closest color for the given
        hex_color.
        E.g. ['#080808',
              '#070707',
              '#0F0F0F',
              '#161616',
              '#1D1D1D',
              '#242424',
              '#2C2C2C',
              '#333333',
              '#3A3A3A',
              '#414141',
              '#484848',
              '#505050',
              '#575757',
              '#5E5E5E',
              '#656565',
              '#6C6C6C',
              '#747474',
              '#7B7B7B',
              '#828282',
              '#898989',
              '#989898']

    Returns
    -------
    The closest hex color in hex_color_list. E.g. #575757.
    """
    color_luminances = [calculate_relative_luminance(x) for x in hex_color_list]
    hex_color_luminance = calculate_relative_luminance(hex_color)
    luminance_distances = [abs(hex_color_luminance - x) for x in color_luminances]

    color_hues = [CU.hex2hls(x)[0] for x in hex_color_list]
    hex_color_hue = CU.hex2hls(hex_color)[0]
    hex_distances = [abs(hex_color_hue - color_hue) for color_hue in color_hues]

    luminance_hue_multi_distances = [
        luminance_distances[i] * hex_distances[i] for i in range(0, len(hex_color_list))
    ]

    color_ratio_map = dict(zip(hex_color_list, luminance_hue_multi_distances))
    sorted_hex_color_list = sorted(hex_color_list, key=lambda x: color_ratio_map[x])
    return sorted_hex_color_list[0]


def convert_hex_to_8bit(hex_color: str) -> int:
    """Convert HEX color string to 8bit color code int value."""
    assert re.match(
        "#[0-9a-zA-Z]{6,8}", hex_color
    ), "f{hex_color} is not a valid HEX color code."
    hex_code_8bits = find_the_cloest_color(hex_color, COLOR_8BIT_HEX_CODE_LIST)
    return COLOR_8BIT_HEX_CODE_LIST.index(hex_code_8bits)


def convert_8bit_to_hex(color_code) -> str:
    """Convert 8bit color code to hex code string."""
    assert 0 <= color_code <= 255, f"{color_code} is not 8bits color code(0 - 255)."
    return COLOR_8BIT_HEX_CODE_LIST[color_code]
