# -*- coding: utf-8 -*-
"""Provides font handling utilities for PDF forms.

This module contains functions for:
- Registering custom fonts from TTF files
- Extracting font information from PDF text appearances
- Calculating font sizes based on widget dimensions
- Adjusting font sizes to fit text within fields
- Managing font colors and properties
"""

from io import BytesIO
from math import sqrt
from re import findall
from typing import Tuple, Union

from reportlab.pdfbase.acroform import AcroForm
from reportlab.pdfbase.pdfmetrics import (registerFont, standardFonts,
                                          stringWidth)
from reportlab.pdfbase.ttfonts import TTFError, TTFont

from .constants import (DEFAULT_FONT, FONT_COLOR_IDENTIFIER,
                        FONT_SIZE_IDENTIFIER, FONT_SIZE_REDUCE_STEP,
                        MARGIN_BETWEEN_LINES, Rect)
from .middleware.text import Text
from .patterns import TEXT_FIELD_APPEARANCE_PATTERNS
from .utils import extract_widget_property


def register_font(font_name: str, ttf_stream: bytes) -> bool:
    """Registers a TrueType font for use in PDF generation.

    Args:
        font_name: Name to register the font under
        ttf_stream: TTF font data as bytes

    Returns:
        bool: True if registration succeeded, False if failed
    """

    buff = BytesIO()
    buff.write(ttf_stream)
    buff.seek(0)

    try:
        registerFont(TTFont(name=font_name, filename=buff))
        result = True
    except TTFError:
        result = False

    buff.close()
    return result


def extract_font_from_text_appearance(text_appearance: str) -> Union[str, None]:
    """Extracts font name from PDF text appearance string.

    Parses the font information embedded in PDF text field appearance strings.

    Args:
        text_appearance: PDF text appearance string (/DA field)

    Returns:
        Union[str, None]: Font name if found, None if not found
    """

    text_appearances = text_appearance.split(" ")

    for each in text_appearances:
        if each.startswith("/"):
            text_segments = findall("[A-Z][^A-Z]*", each.replace("/", ""))

            if len(text_segments) == 1:
                for k, v in AcroForm.formFontNames.items():
                    if v == text_segments[0]:
                        return k

            for font in standardFonts:
                font_segments = findall("[A-Z][^A-Z]*", font.replace("-", ""))
                if len(font_segments) != len(text_segments):
                    continue

                found = True
                for i, val in enumerate(font_segments):
                    if not val.startswith(text_segments[i]):
                        found = False

                if found:
                    return font

    return None


def auto_detect_font(widget: dict) -> str:
    """Attempts to detect the font used in a PDF text field widget.

    Falls back to DEFAULT_FONT if detection fails.

    Args:
        widget: PDF form widget dictionary

    Returns:
        str: Detected font name or DEFAULT_FONT
    """

    text_appearance = extract_widget_property(
        widget, TEXT_FIELD_APPEARANCE_PATTERNS, None, None
    )

    if not text_appearance:
        return DEFAULT_FONT

    return extract_font_from_text_appearance(text_appearance) or DEFAULT_FONT


def text_field_font_size(widget: dict) -> Union[float, int]:
    """Calculates an appropriate font size based on text field dimensions.

    Args:
        widget: PDF form widget dictionary containing Rect coordinates

    Returns:
        Union[float, int]: Suggested font size in points
    """

    height = abs(float(widget[Rect][1]) - float(widget[Rect][3]))

    return height * 2 / 3


def checkbox_radio_font_size(widget: dict) -> Union[float, int]:
    """Calculates appropriate symbol size for checkbox/radio widgets.

    Args:
        widget: PDF form widget dictionary containing Rect coordinates

    Returns:
        Union[float, int]: Suggested symbol size in points
    """

    area = abs(float(widget[Rect][0]) - float(widget[Rect][2])) * abs(
        float(widget[Rect][1]) - float(widget[Rect][3])
    )

    return sqrt(area) * 72 / 96


def get_text_field_font_size(widget: dict) -> Union[float, int]:
    """Extracts font size from PDF text field appearance properties.

    Args:
        widget: PDF form widget dictionary

    Returns:
        Union[float, int]: Font size in points if found, otherwise 0
    """

    result = 0
    text_appearance = extract_widget_property(
        widget, TEXT_FIELD_APPEARANCE_PATTERNS, None, None
    )
    if text_appearance:
        properties = text_appearance.split(" ")
        for i, val in enumerate(properties):
            if val.startswith(FONT_SIZE_IDENTIFIER):
                return float(properties[i - 1])

    return result


def get_text_field_font_color(
    widget: dict,
) -> Union[Tuple[float, float, float], None]:
    """Extracts font color from PDF text field appearance properties.

    Args:
        widget: PDF form widget dictionary

    Returns:
        Union[Tuple[float, float, float], None]: RGB color tuple (0-1 range)
            or black by default if not specified
    """

    result = (0, 0, 0)
    text_appearance = extract_widget_property(
        widget, TEXT_FIELD_APPEARANCE_PATTERNS, None, None
    )
    if text_appearance:
        if FONT_COLOR_IDENTIFIER not in text_appearance:
            return result

        text_appearance = text_appearance.split(" ")
        for i, val in enumerate(text_appearance):
            if val.startswith(FONT_COLOR_IDENTIFIER.replace(" ", "")):
                result = (
                    float(text_appearance[i - 3]),
                    float(text_appearance[i - 2]),
                    float(text_appearance[i - 1]),
                )
                break

    return result


def adjust_paragraph_font_size(widget: dict, widget_middleware: Text) -> None:
    """Dynamically reduces font size until text fits in paragraph field.

    Args:
        widget: PDF form widget dictionary
        widget_middleware: Text middleware instance containing text properties
    """

    # pylint: disable=C0415, R0401
    from .template import get_paragraph_lines

    height = abs(float(widget[Rect][1]) - float(widget[Rect][3]))

    while (
        widget_middleware.font_size > FONT_SIZE_REDUCE_STEP
        and len(widget_middleware.text_lines)
        * (widget_middleware.font_size + MARGIN_BETWEEN_LINES)
        > height
    ):
        widget_middleware.font_size -= FONT_SIZE_REDUCE_STEP
        widget_middleware.text_lines = get_paragraph_lines(widget, widget_middleware)


def adjust_text_field_font_size(widget: dict, widget_middleware: Text) -> None:
    """Dynamically reduces font size until text fits in text field.

    Args:
        widget: PDF form widget dictionary
        widget_middleware: Text middleware instance containing text properties
    """

    width = abs(float(widget[Rect][0]) - float(widget[Rect][2]))

    while (
        widget_middleware.font_size > FONT_SIZE_REDUCE_STEP
        and stringWidth(
            widget_middleware.value, widget_middleware.font, widget_middleware.font_size
        )
        > width
    ):
        widget_middleware.font_size -= FONT_SIZE_REDUCE_STEP
