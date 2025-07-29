#!/usr/bin/env python3

import os
import json
from os.path import abspath, join
from PIL import ImageFont

def get_character_ratios(font_name:str, character:str) -> dict:
    font_file = abspath(join(abspath(join(abspath(__file__), os.pardir)), font_name))
    font = ImageFont.truetype(font_file, 100)
    left, top, right, bottom = font.getbbox(character*10)
    width = float((right-left)/1000) + 0.1
    height = float((bottom-top)/100) + 0.1
    return {"width":width, "height":height}

def get_all_character_ratios(font_name:str, characters:str) -> dict:
    ratios = {}
    widest = {"width":0.0, "height":0.0}
    tallest = {"width":0.0, "height":0.0}
    for character in characters:
        ratios[character] = get_character_ratios(font_name, character)
        if ratios[character]["width"] > widest["width"]:
            widest = ratios[character]
        if ratios[character]["height"] > tallest["height"]:
            tallest = ratios[character]
    ratios["widest"] = widest
    ratios["tallest"] = tallest
    return ratios

def get_all_characters() -> str:
    characters = " €Ž"
    for i in range(33, 127):
        characters = f"{characters}{chr(i)}"
    for i in range(161, 256):
        characters = f"{characters}{chr(i)}"
    return characters

def main():
    ratios = get_all_character_ratios("NotoSerif-BoldItalic.ttf", get_all_characters())
    json_file = abspath(join(abspath(join(abspath(__file__), os.pardir)), "NotoSerif-BoldItalic.json"))
    with open(json_file, "w", encoding="UTF-8") as out_file:
        out_file.write(json.dumps(ratios, indent="   ", separators=(", ", ": ")))

if __name__ == "__main__":
    main()