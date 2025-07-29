#!/usr/bin/env python3

import os
import re
import math
import argparse
import cairosvg
import random
import tempfile
import html_string_tools
import cover_generator.color as cc
import cover_generator.font_handling as fh
from os.path import abspath, exists, join
from PIL import Image

def get_multiline_svg(text:str, glyph_sizes:dict, x:int, y:int, width:int, height:int,
            font_style:str, max_lines:int=3, height_multiplier:float=1.1,
            text_anchor:str="middle", dominant_baseline:str="central") -> str:
    """
    Creates a text element for given text in an SVG file, creating multiple lines if necessary

    :param text: Text to convert into svg
    :type text: str, required
    :param glyph_sizes: Dictionary of width and height for each glyph
    :type glyph_sizes: dict, required
    :param x: X position of the text element
    :type x: int, required
    :param y: Y position of the text element
    :type y: int required
    :param width: Width of the area to fit text into
    :type width: int, required
    :param height: Height of the area to fit text into
    :type height: int, required
    :param font_style: CSS Style of the font minus font-size
    :type font_style: str, required
    :param max_lines: Maximum number of lines of text allowed, defaults to 3
    :type max_lines: int, optional
    :param height_multiplier: Value to multiply with text size to get height of a line, defaults to 1.1
    :type height_multiplier: float, optional
    :param text_anchor: Text Anchor alignment for the text element, defaults to "middle"
    :type text_anchor: str, optional
    :param dominant_baseline: Dominant Baseline alignment for the text element, defaults to "central"
    :type dominant_baseline: str, optional
    :return: SVG text element
    :rtype: str
    """
    # Get lines and text size from the initial text
    lines = fh.max_word_wrap(text, glyph_sizes, max_lines=max_lines)
    text_size = fh.get_text_size(lines, glyph_sizes, width, height, height_multiplier=height_multiplier)
    # Replace all non-ASCII characters with XML/HTML escape characters
    for i in range(0, len(lines)):
        lines[i] = html_string_tools.replace_reserved_characters(lines[i], True)
    # Get the height of one line
    line_height = math.floor(text_size * height_multiplier)
    if len(lines) == 1:
        line_height = text_size
    # Get the tspan tags
    start_y = 0
    if dominant_baseline == "central":
        start_y = 0 - math.floor((line_height/2) * (len(lines) - 1))
    next_y = line_height
    if dominant_baseline == "alphabetic":
        next_y = 0 - line_height
        lines = lines[::-1]
    svg = f"<tspan x=\"{x}\" dy=\"{start_y}\">{lines[0]}</tspan>"
    for i in range(1, len(lines)):
        svg = f"{svg}<tspan x=\"{x}\" dy=\"{next_y}\">{lines[i]}</tspan>"
    # Create the main text tag
    text_header = f"<text y=\"{y}\" text-anchor=\"{text_anchor}\""
    text_header = f"{text_header} dominant-baseline=\"{dominant_baseline}\""
    text_header = f"{text_header} style=\"font-size:{text_size}px;{font_style}\">"
    # Combine inner and outer text for the final text tag
    svg = f"{text_header}{svg}</text>"
    return svg

def generate_border_layout(title:str, author:str, background_color:str, foreground_color:str) -> str:
    """
    Generates an SVG cover image in the border layout.

    :param title: Title of the book/media
    :type title: str, required
    :param author: Author(s) of the book/media
    :type author: str, required
    :param background_color: Background color in hex code format (#RRGGBB)
    :type background_color: str, required
    :param foreground_color: Foreground color in hex code format (#RRGGBB - Used for border)
    :type foreground_color: str, required
    :return: Cover image in SVG format
    :rtype: str
    """
    # Get sizes for the font profile
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-Bold.json")
    # Create the background
    svg = f"<defs><style type=\"text/css\" /></defs>"
    svg = f"{svg}<rect x=\"-1\" y=\"-1\" width=\"1202\" height=\"1602\" fill=\"{background_color}\"/>"
    # Create the border
    svg = f"{svg}<rect x=\"20\" y=\"20\" width=\"1160\" height=\"1560\" fill=\"{foreground_color}\"/>"
    svg = f"{svg}<rect x=\"40\" y=\"40\" width=\"1120\" height=\"1520\" fill=\"{background_color}\"/>"
    svg = f"{svg}<rect x=\"50\" y=\"50\" width=\"1100\" height=\"1500\" fill=\"{foreground_color}\"/>"
    svg = f"{svg}<rect x=\"60\" y=\"60\" width=\"1080\" height=\"1480\" fill=\"{background_color}\"/>"
    # Create the middle separator element
    separator = f"<polygon points=\"120,15 125,10 560,5 570,15 560,25 125,20\" fill=\"{foreground_color}\" />"
    separator = f"{separator}<polygon points=\"1080,15 1075,10 640,5 630,15 640,25 1075,20\""
    separator = f"{separator} fill=\"{foreground_color}\" />"
    separator = f"{separator}<circle cx=\"600\" cy=\"15\" r=\"15\" fill=\"{foreground_color}\" />"
    separator = f"<g transform=\"translate(0, 785)\">{separator}</g>"
    # Create the title text
    text_color = cc.get_text_color(background_color)
    font_style = f"font-style:normal;font-weight:bold;font-family:Noto Serif,Serif;fill:{text_color}"
    max_lines = fh.get_optimized_line_number(title.upper(), glyph_sizes)
    title_svg = get_multiline_svg(title.upper(), glyph_sizes, 600, 705, width=960, height=740,
            font_style=font_style, text_anchor="middle", dominant_baseline="alphabetic", max_lines=max_lines)
    # Create the author text
    author_svg = get_multiline_svg(author.upper(), glyph_sizes, 600, 845, width=960, height=400,
            font_style=font_style, text_anchor="middle", dominant_baseline="hanging", max_lines=2)
    # Offset the full text block
    title_lines = len(re.findall(r"<tspan", title_svg))
    title_font_size = int(re.findall("(?<=style=\"font-size:)[0-9]+(?=px)", title_svg)[0])
    title_height = (title_lines * title_font_size) * 1.1
    author_lines = len(re.findall(r"<tspan", author_svg))
    author_font_size = int(re.findall("(?<=style=\"font-size:)[0-9]+(?=px)", author_svg)[0])
    author_height = (author_lines * author_font_size) * 1.1
    block_offset = math.floor((title_height - author_height) / 3)
    text_block = f"<g transform=\"translate(0, {block_offset})\">{title_svg}{separator}{author_svg}</g>"
    svg = f"{svg}{text_block}"
    # Encapsulate the SVG
    svg = f"<svg viewBox=\"0 0 1200 1600\" xmlns=\"http://www.w3.org/2000/svg\">{svg}</svg>"
    return svg

def generate_bubble_layout(title:str, author:str, background_color:str, foreground_color:str) -> str:
    """
    Generates an SVG cover image in the bubble layout.

    :param title: Title of the book/media
    :type title: str, required
    :param author: Author(s) of the book/media
    :type author: str, required
    :param background_color: Background color in hex code format (#RRGGBB)
    :type background_color: str, required
    :param foreground_color: Foreground color in hex code format (#RRGGBB - Used for bubble)
    :type foreground_color: str, required
    :return: Cover image in SVG format
    :rtype: str
    """
    # Get the font glyph sizes
    bold_glyph_sizes = fh.get_glyph_sizes("NotoSerif-Bold.ttf")
    italic_glyph_sizes = fh.get_glyph_sizes("NotoSerif-BoldItalic.ttf")
    # Create the background
    svg = f"<defs><style type=\"text/css\" /></defs>"
    svg = f"{svg}<rect x=\"-1\" y=\"-1\" width=\"1202\" height=\"1602\" fill=\"{background_color}\" />"
    # Create the title text
    text_color = cc.get_text_color(foreground_color)
    font_style = f"font-style:italic;font-weight:bold;font-family:Noto Serif,Serif;fill:{text_color}"
    max_lines = fh.get_optimized_line_number(title.upper(), italic_glyph_sizes)
    title_svg = get_multiline_svg(title.upper(), italic_glyph_sizes, 600, 0, width=980, height=1000,
            font_style=font_style, text_anchor="middle", dominant_baseline="central", max_lines=max_lines)
    # Create the title bubble
    title_lines = len(re.findall(r"<tspan", title_svg))
    title_font_size = int(re.findall("(?<=style=\"font-size:)[0-9]+(?=px)", title_svg)[0])
    bubble_height = (title_font_size * title_lines) + 80
    if bubble_height < 500:
        bubble_height = 500
    bubble_svg = f"<rect x=\"80\" y=\"0\" width=\"1040\" height=\"{bubble_height}\" rx=\"40\" ry=\"40\" "
    bubble_svg = f"{bubble_svg}fill=\"{foreground_color}\" />"
    # Create the author text
    text_color = cc.get_text_color(background_color)
    font_style = f"font-style:normal;font-weight:bold;font-family:Noto Serif,Serif;fill:{text_color}"
    author_svg = get_multiline_svg(author.upper(), bold_glyph_sizes, 600, 1540, width=1100, height=400,
            font_style=font_style, text_anchor="middle", dominant_baseline="alphabetic", max_lines=2)
    svg = f"{svg}{author_svg}"
    # Create full bubble section
    y = math.floor(bubble_height/2)
    full_bubble = f"{bubble_svg}<g transform=\"translate(0, {y})\">{title_svg}</g>"
    author_lines = len(re.findall(r"<tspan", author_svg))
    author_font_size = int(re.findall("(?<=style=\"font-size:)[0-9]+(?=px)", author_svg)[0])
    author_height = author_lines * author_font_size
    bubble_offset = math.floor(((1540 - author_height) - bubble_height) / 3)
    full_bubble = f"<g transform=\"translate(0 {bubble_offset})\">{full_bubble}</g>"
    svg = f"{svg}{full_bubble}"
    
    
    # Encapsulate the svg file
    svg = f"<svg viewBox=\"0 0 1200 1600\" xmlns=\"http://www.w3.org/2000/svg\">{svg}</svg>"
    return svg

def generate_cross_layout(title:str, author:str, background_color:str, foreground_color:str) -> str:
    """
    Generates an SVG cover image in the cross layout.

    :param title: Title of the book/media
    :type title: str, required
    :param author: Author(s) of the book/media
    :type author: str, required
    :param background_color: Background color in hex code format (#RRGGBB)
    :type background_color: str, required
    :param foreground_color: Foreground color in hex code format (#RRGGBB - Used for cross)
    :type foreground_color: str, required
    :return: Cover image in SVG format
    :rtype: str
    """
    # Get the font glyph sizes
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-BoldItalic.ttf")
    # Create the background
    svg = f"<defs><style type=\"text/css\" /></defs>"
    svg = f"{svg}<rect x=\"-1\" y=\"-1\" width=\"1202\" height=\"1602\" fill=\"{background_color}\" />"
    # Create the cross
    svg = f"{svg}<rect x=\"240\" y=\"-1\" width=\"80\" height=\"1602\" fill=\"{foreground_color}\" />"
    svg = f"{svg}<rect x=\"-1\" y=\"380\" width=\"1202\" height=\"80\" fill=\"{foreground_color}\" />"
    # Create the title element
    text_color = cc.get_text_color(background_color)
    font_style = f"font-style:italic;font-weight:bold;font-family:Noto Serif,Serif;fill:{text_color}"
    max_lines = fh.get_optimized_line_number(title, glyph_sizes)
    title_svg = get_multiline_svg(title, glyph_sizes, 380, 480, width=820, height=800,
            font_style=font_style, text_anchor="start", dominant_baseline="hanging", max_lines=max_lines)
    svg = f"{svg}{title_svg}"
    # Create the author element
    author_svg = get_multiline_svg(author, glyph_sizes, 380, 300, width=820, height=280,
            font_style=font_style, text_anchor="start", dominant_baseline="alphabetic", max_lines=2)
    svg = f"{svg}{author_svg}"
    # Encapsulate the svg file
    svg = f"<svg viewBox=\"0 0 1200 1600\" xmlns=\"http://www.w3.org/2000/svg\">{svg}</svg>"
    return svg

def write_layout_to_image(svg:str, path:str, width:int=1200) -> bool:
    """
    Writes a given SVG cover image as an image file.

    :param svg: Cover image layout in SVG format
    :type svg: str, required
    :param path: Absolute path of the image file to save
    :type path: str, required
    :param width: Width of the image, defaults to 1200
    :type width: int, optional
    :return: Whether saving the image was successful
    :rtype: bool
    """
    # Create a temporary directory to save the base file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write the svg file
        svg_file = abspath(join(temp_dir, "base.svg"))
        with open(svg_file, "w", encoding="UTF-8") as out_file:
            out_file.write(svg)
        assert exists(svg_file)
        # Convert to a png file using cairosvg
        base_image_file = abspath(join(temp_dir, "base.png"))
        cairosvg.svg2png(url=svg_file, write_to=base_image_file)
        # Load as PIL image
        image = Image.open(base_image_file)
        # Resize if necessary
        if not width == image.size[0]:
            ratio = width/image.size[0]
            height = int(image.size[1] * ratio)
            image = image.resize(size=(width, height))
        # Save to the given path
        if path.endswith(".jpg") or path.endswith(".jpeg"):
            image.save(abspath(path), quality=95, compress_level=9)
        elif path.endswith(".png"):
            image.save(abspath(path), optimize=True)
        else:
            image.save(abspath(path))
        return exists(abspath(path))

def generate_cover(title:str, author:str, path:str, width:int=1200, cover_style:str=None,
            palette_category:str=None, palette_name:str=None, color_id:str=None) -> bool:
    """
    Generates a book cover image based on a given title and author.
    Color palette and cover style are picked at random if not specified.
    
    :param title: Title of the book/media
    :type title: str, required
    :param author: Author(s) of the book/media
    :type author: str, required
    :param path: Absolute path of the image file to save
    :type path: str, required
    :param width: Width of the image, defaults to 1200
    :type width: int, optional
    :param cover_style: Style of the cover ("border", "bubble", or "cross"), defaults to None
    :type cover_style: str, optional
    :param palette_category: Palette Category limit, defaults to None
    :type palette_category: str, optional
    :param palette_name: Palette Name limit, defaults to None
    :type palette_name: str, optional
    :param color_id: Color ID limit, defaults to None
    :type color_id: str, optional
    :return: Whether saving the image was successful
    :rtype: bool 
    """
    # Get color palette
    background, foreground = cc.get_color_pair(palette_category, palette_name, color_id)
    # Determine the cover style
    try:
        style = cover_style.lower().strip()
    except AttributeError: style = ""
    styles = ["border", "bubble", "cross"]
    if style is None or not style in styles:
        style = styles[random.randrange(0, len(styles))]
    # Generate the cover based on style
    if style == "border":
        svg = generate_border_layout(title, author, background, foreground)
    if style == "bubble":
        svg = generate_bubble_layout(title, author, background, foreground)
    if style == "cross":
        svg = generate_cross_layout(title, author, background, foreground)
    # Save the cover as an image file
    return write_layout_to_image(svg, path, width=width)

def main():
    """
    Sets up the parser for the user generate cover images.
    """
    # Set up argument parser
    categories = []
    for palette in cc.get_all_palettes():
        if not palette["category"] in categories:
            categories.append(palette["category"])
    help_text = ", ".join(sorted(categories))
    help_text = f"Styles: border, bubble, cross | Palettes: {help_text}"
    parser = argparse.ArgumentParser(epilog=help_text)
    parser.add_argument(
        "-t",
        "--title",
        help="Title of the book/media",
        type=str,
        required=True)
    parser.add_argument(
        "-a",
        "--author",
        help="Author of the book/media",
        type=str,
        required=True)
    parser.add_argument(
        "-o",
        "--output",
        help="Output image file",
        nargs="?",
        type=str,
        default=join(abspath(os.getcwd()), "cover.png"))
    parser.add_argument(
        "-w",
        "--width",
        help="Width of the image in pixels",
        nargs="?",
        type=int,
        default=1200)
    parser.add_argument(
        "-s",
        "--style",
        help="Cover Style (border, bubble, cross)",
        nargs="?",
        type=str,
        default=None)
    parser.add_argument(
        "-p",
        "--palette",
        help="Palette Category",
        nargs="?",
        type=str,
        default=None)
    args = parser.parse_args()
    generate_cover(args.title, args.author, abspath(args.output), width=args.width,
            cover_style=args.style, palette_category=args.palette)
        
