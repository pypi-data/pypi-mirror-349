#!/usr/bin/env python3

import os
import re
import json
import math
from os.path import abspath, exists, join
from typing import List

FONT_DIRECTORY = abspath(join(abspath(join(abspath(__file__), os.pardir)), "fonts"))
assert exists(FONT_DIRECTORY)

def get_glyph_sizes(font_name:str) -> dict:
    """
    Get a dictionary of glyph sizes from a given JSON file or associated font file.
    Grabs the file from the internal font directory.

    :param font_name: Filename of the font
    :type font_name: str, required
    :return: Dictionary of glyphs with corresponding relative sizes
    :rtype: dict
    """
    # Get the base filename
    filename = re.sub(r"\..{1,5}$", "", font_name)
    filename = f"{filename}.json"
    # Read the JSON file
    json_file = abspath(join(FONT_DIRECTORY, filename))
    with open(json_file) as jf:
        glyph_sizes = json.loads(jf.read())
    # Return the dictionary
    return glyph_sizes

def get_string_size(text:str, glyph_sizes:dict) -> (float, float):
    """
    Returns the width and height of a line of text based on the given sizes of each character.

    :param text: Line of text from which to get the size
    :type text: str, required
    :param glyph_sizes: Dictionary of width and height for each glyph
    :type glyph_sizes: dict, required
    :return: Tuple of (width, height)
    :rtype: (float, float)
    """
    # Run through each character to update width and height
    width = 0
    height = 0
    for character in text:
        try:
            character_size = glyph_sizes[character]
        except KeyError:
            # Get values for the largest glyph if character not found
            character_size = {}
            character_size["width"] = glyph_sizes["widest"]["width"]
            character_size["height"] = glyph_sizes["tallest"]["height"]
        # Update width and height
        width += character_size["width"]
        if character_size["height"] > height:
            height = character_size["height"]
    # Return the width and height
    return round(width, 4), round(height, 4)

def get_largest_line_size(lines:List[str], glyph_sizes:dict) -> (float, float):
    """
    Returns the largest width and height of a line in a list of lines.
    Largest width and height don't necessarily belong to the same line.

    :param lines: List of strings
    :type lines: List[str], required
    :param glyph_sizes: Dictionary of width and height for each glyph
    :type glyph_sizes: dict, required
    :return: Tuple of (Largest Width, Largest Height)
    :rtype: (float, float)
    """
    width = 0
    height = 0
    for line in lines:
        test_width, test_height = get_string_size(line, glyph_sizes)
        if test_width > width:
            width = test_width
        if test_height > height:
            height = test_height
    return width, height

def word_wrap(text:str, glyph_sizes:dict, max_width:float) -> List[str]:
    """
    Splits given text into lines based on a limit on how wide each line can be.

    :param text: Text to split into lines
    :type text: str, required
    :param glyph_sizes: Dictionary of width and height for each glyph
    :type glyph_sizes: dict, required
    :param max_width: Width a line can reach before rolling over to the next line.
    :type max_width: float, required
    :return: Text divided into lines
    :rtype: List[str]
    """
    # Split up text into separate "words"
    clean_text = re.sub(r"\s+", " ", text).strip()
    words = clean_text.split(" ")
    # Start wrapping text
    lines = []
    current_line = ""
    while len(words) > 0:
        test_line = f"{current_line} {words[0]}".strip()
        test_width = get_string_size(test_line, glyph_sizes)[0]
        if test_width > max_width and not current_line == "":
            lines.append(current_line)
            test_line = words[0]
        current_line = test_line
        del words[0]
    # Add remaining text
    if not current_line == "":
        lines.append(current_line)
    # Return the lines
    return lines

def max_word_wrap(text:str, glyph_sizes:dict, min_width:float=4.0, max_lines:int=3) -> List[str]:
    """
    Splits given text into lines, with each line allowing at least the minimum width.
    Lines will allow at least as wide as the width of the longest word in the string.

    :param text: Text to be split into multiple lines
    :type text: str, required
    :param glyph_sizes: Dictionary of width and height for each glyph
    :type glyph_sizes: dict, required
    :param min_width: Minimum width to allow on a line, defaults to 3.0
    :type min_width: float, optional
    :param max_lines: Maximum number of lines allowed, defaults to 3
    :type max_lines: int, optional
    :return: List of strings representing individual lines
    :rytpe: List[str]
    """
    # Get the longest character string in the given text
    clean_text = re.sub(r"\s+", " ", text).strip()
    clean_text = re.sub(r"\s+-\s+", ": ", clean_text)
    width_limit = get_largest_line_size(clean_text.split(" "), glyph_sizes)[0]
    # Make sure the character limit doesn't fall below the given minimum
    if width_limit < min_width:
        width_limit = min_width
    # Wrap the text
    lines = word_wrap(clean_text, glyph_sizes, width_limit)
    # Format strings with colons separately, if applicable
    if ":" in clean_text:
        lines = []
        separated = clean_text.split(":")
        for i in range(0, len(separated) - 1):
            lines.extend(max_word_wrap(f"{separated[i]}!", glyph_sizes, width_limit, max_lines))
            lines[-1] = lines[-1][:-1] + ":"
        lines.extend(max_word_wrap(separated[-1], glyph_sizes, width_limit, max_lines))
    # Re-wrap if there are more than the allowed number of lines
    if len(lines) > max_lines:
        lines = max_word_wrap(text, glyph_sizes, min_width + 0.5, max_lines)
    # Return the text with word wrapping
    return lines

def get_optimized_line_number(text:str, glyph_sizes:dict) -> int:
    """
    Determine the optimized maximum number of lines for a given text
    
    :param text: Text to be split into multiple lines
    :type text: str, required
    :param glyph_sizes: Dictionary of width and height for each glyph
    :type glyph_sizes: dict, required
    :return: Maximum number of lines
    :rytpe: int
    """
    # Determine the maximum number of lines appropriate for the text
    width = get_string_size(re.sub(r"\s+", " ", text).strip(), glyph_sizes)[0]
    max_lines = math.floor(width / 6)
    # Adjust the max lines if it is too small or too big
    if max_lines < 3:
        max_lines = 3
    if max_lines > 6:
        max_lines = 6
    # Return the maximum line number
    return max_lines

def get_text_size(lines:str, glyph_sizes:dict, width:int, height:int,
            height_multiplier:float=1.1) -> int:
    """
    Returns the largest text size that can fit in a given height and width with a given font.

    :param lines: Lines of text to check for width and height
    :type lines: List[str], required
    :param glyph_sizes: Dictionary of width and height for each glyph
    :type glyph_sizes: dict, required
    :param width: Width of the area to fit text into
    :type width: int, required
    :param height: Height of the area to fit text into
    :type height: int, required
    :param height_multiplier: Value to multiply with text size to get height of a line, defaults to 1.1
    :type height_multiplier: float, optional
    :return: Maximum text size
    :rtype: int
    """
    # Get base text size based on the longest line
    widest = get_largest_line_size(lines, glyph_sizes)[0]
    base_width = math.floor(width/widest)
    # Get base text size based on the number of lines
    base_height = height
    if len(lines) > 1:
        base_height = math.floor(height / (height_multiplier * len(lines)))
    # Return the lower text size
    if base_height < base_width:
        return base_height
    return base_width
