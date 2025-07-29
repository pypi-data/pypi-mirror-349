#!/usr/bin/env python3

import os
import json
import math
import colorsys
import random
from os.path import abspath, exists, isdir, join
from typing import List

PALETTE_DIRECTORY = abspath(join(abspath(join(abspath(__file__), os.pardir)), "palettes"))
assert exists(PALETTE_DIRECTORY)

def rgb_to_hex(red:float, green:float, blue:float) -> str:
    """
    Converts raw red green and blue values to hex color code.

    :param red: Red value (0.0 to 1.0)
    :type red: float, required
    :param green: Green value (0.0 to 1.0)
    :type green: float, required
    :param blue: Blue value (0.0 to 1.0)
    :type blue: float, required
    :return: Hex color code (#RRGGBB)
    :rtype: str
    """
    hex_red = str(hex(math.floor(red*255))[2:]).zfill(2).lower()
    hex_green = str(hex(math.floor(green*255))[2:]).zfill(2).lower()
    hex_blue = str(hex(math.floor(blue*255))[2:]).zfill(2).lower()
    return f"#{hex_red}{hex_green}{hex_blue}"

def get_text_color(background_color:str) -> str:
    """
    Returns either contrasting color for text based off a given background color.
    Returns either black or white

    :param background_color: Background color as Hex color
    :type background_color: str, requred
    :return: Hex color code for the text color
    :rtype: str
    """
    # Get the HSV value of the color
    red = float(int(background_color[1:3], 16)/255)
    green = float(int(background_color[3:5], 16)/255)
    blue = float(int(background_color[5:7], 16)/255)
    h, s, v = colorsys.rgb_to_hsv(red, green, blue)
    # Return black if the color is light enough
    if v > 0.5:
        return "#000000"
    # Return white if the color is dark enough
    return "#ffffff"

def get_all_palettes() -> List[dict]:
    """
    Returns a list of all the embedded palettes available.
    
    :return: List of dictionaries for all embedded palettes.
    :rytpe: List[dict]
    """
    # Get all palette JSON files
    jsons = []
    directories = [PALETTE_DIRECTORY]
    while len(directories) > 0:
        files = sorted(os.listdir(directories[0]))
        for file in files:
            full_file = abspath(join(directories[0], file))
            if full_file.endswith(".json"):
                jsons.append(full_file)
            elif isdir(full_file):
                directories.append(full_file)
        del directories[0]
    # Read JSON files
    palettes = []
    for json_file in jsons:
        with open(json_file) as jf:
            palette = json.loads(jf.read())
        palettes.append(palette)
    return palettes

def get_color_pair(palette_category:str=None, palette_name:str=None, color_id:str=None) -> (str, str):
    """
    Returns a random color pair containing a primary and secondary color based on embedded palettes.
    Color selection can be limited by category, specific palette, and/or exact color ID.
    If any limit is set to None, that value will be random.
    
    :param palette_category: Palette Category limit, defaults to None
    :type palette_category: str, optional
    :param palette_name: Palette Name limit, defaults to None
    :type palette_name: str, optional
    :param color_id: Color ID limit, defaults to None
    :type color_id: str, optional
    :return: Tuple of (Primary Color, Secondary Color) in hex color format
    :rtype: (str, str)
    """
    # Get a list of all available palettes
    palettes = get_all_palettes()
    # Remove all palettes that don't fit the palette category or palette name
    for i in range(len(palettes) - 1, -1, -1):
        if palette_category is not None and not palettes[i]["category"] == palette_category:
            del palettes[i]
            continue
        if palette_name is not None and not palettes[i]["name"] == palette_name:
            del palettes[i]
    # Extract the color pairs
    color_pairs = []
    for palette in palettes:
        color_pairs.extend(palette["color_pairs"])
    # Remove color pairs that don't match the given id
    try:
        id_value = int(color_id)
    except (TypeError, ValueError): id_value = None
    for i in range(len(color_pairs) - 1, -1, -1):
        if id_value is not None and not color_pairs[i]["id"] == id_value:
            del color_pairs[i]
    # Return black and white palette if no color pairs are left
    if len(color_pairs) == 0:
        return "#ffffff", "#000000"
    # Select a random color pair to return
    color_pair = color_pairs[random.randrange(0, len(color_pairs))]
    return color_pair["primary_color"], color_pair["secondary_color"]

def get_hue_offset(hue:float, hue_offset:float) -> float:
    """
    Adds a given hue offset to a hue value to get a new hue.
    Hue value is wrapped around to an acceptable value if not between 0.0 and 1.0
    
    :param hue: Starting hue value 
    :type hue: float, required
    :param hue_offset: Amount to offset the hue by
    :type hue_offset: float, required
    :return: New hue value
    :rtype: float
    """
    new_hue = hue + hue_offset
    while new_hue > 1:
        new_hue -= 1
    while new_hue < 0:
        new_hue += 1
    return round(new_hue, 4)

def generate_offset_palette(palette_name:str, palette_category:str, hue_offset:float,
            primary_saturation:float, primary_value:float,
            secondary_saturation:float, secondary_value:float) -> dict:
    """
    Generates a palette where each primary color has a secondary color with a given hue offset from the primary.
    Creates a primary and secondary color for 30 hues on the color wheel.
    
    :param palette_name: Name of the generated palette
    :type palette_name: str, required
    :param palette_category: Name of the palette category
    :type palette_category: str, required
    :param primary_saturation: Saturation for the primary color
    :type primary_saturation: float, required
    :param primary_value: Value (Lightness) for the primary color
    :type primary_value: float, required
    :param secondary_saturation: Saturation for the secondary color
    :type secondary_saturation: float, required
    :param secondary_value: Value (Lightness) for the secondary color
    :type secondary_value: float, required
    :return: Dictionary containing all of the palette information
    :rtype: dict
    """
    palette = {"name":palette_name, "category":palette_category}
    color_pairs = []
    for i in range(0, 30):
        # Get the primary color
        primary_hue = i*(1/30)
        r, g, b = colorsys.hsv_to_rgb(primary_hue, primary_saturation, primary_value)
        primary_color = rgb_to_hex(r, g, b)
        # Get the secondary_color
        secondary_hue = get_hue_offset(primary_hue, hue_offset)
        r, g, b = colorsys.hsv_to_rgb(secondary_hue, secondary_saturation, secondary_value)
        secondary_color = rgb_to_hex(r, g, b)
        # Set the values in the palette
        color_pair = {"id":i, "primary_color": primary_color, "secondary_color":secondary_color}
        color_pairs.append(color_pair)
    palette["color_pairs"] = color_pairs
    return palette
