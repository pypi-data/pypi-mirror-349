#!/usr/bin/env python3

import os
import tempfile
import cover_generator.cover_generator as cg
import cover_generator.font_handling as fh
from os.path import abspath, join
from PIL import Image

def test_get_multiline_svg():
    """
    Tests the get_multiline_svg function.
    """
    # Test getting multiline svg with base settings.
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-Bold.ttf")
    text = "Just some words."
    font_style = "fill:#FFFFFF;font-family:Serif"
    svg = cg.get_multiline_svg(text, glyph_sizes, 600, 300, width=1040, height=700,
        font_style=font_style)
    compare = "<text y=\"300\" text-anchor=\"middle\" dominant-baseline=\"central\" "
    compare = f"{compare}style=\"font-size:212px;fill:#FFFFFF;font-family:Serif\">"
    compare = f"{compare}<tspan x=\"600\" dy=\"-233\">Just</tspan>"
    compare = f"{compare}<tspan x=\"600\" dy=\"233\">some</tspan>"
    compare = f"{compare}<tspan x=\"600\" dy=\"233\">words.</tspan></text>"
    assert svg == compare
    # Test hanging vertical alignment and start horizontal alignment
    svg = cg.get_multiline_svg(text, glyph_sizes, 0, 50, width=600, height=700, font_style=font_style,
            text_anchor="start", dominant_baseline="hanging", max_lines=2)
    compare = "<text y=\"50\" text-anchor=\"start\" dominant-baseline=\"hanging\" "
    compare = f"{compare}style=\"font-size:103px;fill:#FFFFFF;font-family:Serif\">"
    compare = f"{compare}<tspan x=\"0\" dy=\"0\">Just some</tspan>"
    compare = f"{compare}<tspan x=\"0\" dy=\"113\">words.</tspan></text>"
    assert svg == compare
    # Test center vertical alignment and middle horizontal alignment
    svg = cg.get_multiline_svg(text, glyph_sizes, 500, 300, width=1000, height=700,
            font_style=font_style, text_anchor="middle", dominant_baseline="center")
    compare = "<text y=\"300\" text-anchor=\"middle\" dominant-baseline=\"center\" "
    compare = f"{compare}style=\"font-size:212px;fill:#FFFFFF;font-family:Serif\">"
    compare = f"{compare}<tspan x=\"500\" dy=\"0\">Just</tspan>"
    compare = f"{compare}<tspan x=\"500\" dy=\"233\">some</tspan>"
    compare = f"{compare}<tspan x=\"500\" dy=\"233\">words.</tspan></text>"
    assert svg == compare
    # Test alphabetic vertical alignment and end horizontal alignment
    svg = cg.get_multiline_svg(text, glyph_sizes, 1200, 1600, width=800, height=700,
        font_style=font_style, text_anchor="end", dominant_baseline="alphabetic")
    compare = "<text y=\"1600\" text-anchor=\"end\" dominant-baseline=\"alphabetic\" "
    compare = f"{compare}style=\"font-size:198px;fill:#FFFFFF;font-family:Serif\">"
    compare = f"{compare}<tspan x=\"1200\" dy=\"0\">words.</tspan>"
    compare = f"{compare}<tspan x=\"1200\" dy=\"-217\">some</tspan>"
    compare = f"{compare}<tspan x=\"1200\" dy=\"-217\">Just</tspan></text>"
    assert svg == compare
    # Test that special characters are escaped
    text = "This & That"
    svg = cg.get_multiline_svg(text, glyph_sizes, 600, 300, width=1040, height=700,
            font_style=font_style, max_lines=2)
    compare = "<text y=\"300\" text-anchor=\"middle\" dominant-baseline=\"central\" "
    compare = f"{compare}style=\"font-size:272px;fill:#FFFFFF;font-family:Serif\">"
    compare = f"{compare}<tspan x=\"600\" dy=\"-149\">This &#38;</tspan>"
    compare = f"{compare}<tspan x=\"600\" dy=\"299\">That</tspan></text>"
    assert svg == compare

def test_generate_border_layout():
    """
    Tests the generate_border_layout function.
    """
    border = cg.generate_border_layout("A simple title", "Author",
            background_color="#e01010", foreground_color="#004e00")
    compare = "<svg viewBox=\"0 0 1200 1600\" xmlns=\"http://www.w3.org/2000/svg\">"
    compare = f"{compare}<defs><style type=\"text/css\" /></defs>"
    compare = f"{compare}<rect x=\"-1\" y=\"-1\" width=\"1202\" height=\"1602\" fill=\"#e01010\"/>"
    compare = f"{compare}<rect x=\"20\" y=\"20\" width=\"1160\" height=\"1560\" fill=\"#004e00\"/>"
    compare = f"{compare}<rect x=\"40\" y=\"40\" width=\"1120\" height=\"1520\" fill=\"#e01010\"/>"
    compare = f"{compare}<rect x=\"50\" y=\"50\" width=\"1100\" height=\"1500\" fill=\"#004e00\"/>"
    compare = f"{compare}<rect x=\"60\" y=\"60\" width=\"1080\" height=\"1480\" fill=\"#e01010\"/>"
    compare = f"{compare}<g transform=\"translate(0, 166)\">"
    compare = f"{compare}<text y=\"705\" text-anchor=\"middle\" dominant-baseline=\"alphabetic\" "
    compare = f"{compare}style=\"font-size:214px;font-style:normal;font-weight:bold;"
    compare = f"{compare}font-family:Noto Serif,Serif;fill:#000000\">"
    compare = f"{compare}<tspan x=\"600\" dy=\"0\">TITLE</tspan><tspan x=\"600\" dy=\"-235\">SIMPLE</tspan>"
    compare = f"{compare}<tspan x=\"600\" dy=\"-235\">A</tspan></text>"
    compare = f"{compare}<g transform=\"translate(0, 785)\">"
    compare = f"{compare}<polygon points=\"120,15 125,10 560,5 570,15 560,25 125,20\" fill=\"#004e00\" />"
    compare = f"{compare}<polygon points=\"1080,15 1075,10 640,5 630,15 640,25 1075,20\" fill=\"#004e00\" />"
    compare = f"{compare}<circle cx=\"600\" cy=\"15\" r=\"15\" fill=\"#004e00\" /></g>"
    compare = f"{compare}<text y=\"845\" text-anchor=\"middle\" dominant-baseline=\"hanging\" "
    compare = f"{compare}style=\"font-size:189px;font-style:normal;font-weight:bold;"
    compare = f"{compare}font-family:Noto Serif,Serif;fill:#000000\">"
    compare = f"{compare}<tspan x=\"600\" dy=\"0\">AUTHOR</tspan></text></g></svg>"
    assert border == compare

def test_generate_bubble_layout():
    """
    Tests the generate_bubble_layout fuction.
    """
    bubble = cg.generate_bubble_layout("Some Title", "Artist",
            background_color="#000030", foreground_color="#ff0000")
    compare = "<svg viewBox=\"0 0 1200 1600\" xmlns=\"http://www.w3.org/2000/svg\">"
    compare = f"{compare}<defs><style type=\"text/css\" />"
    compare = f"{compare}</defs><rect x=\"-1\" y=\"-1\" width=\"1202\" height=\"1602\" fill=\"#000030\" />"
    compare = f"{compare}<text y=\"1540\" text-anchor=\"middle\" dominant-baseline=\"alphabetic\" "
    compare = f"{compare}style=\"font-size:252px;font-style:normal;font-weight:bold;"
    compare = f"{compare}font-family:Noto Serif,Serif;fill:#ffffff\">"
    compare = f"{compare}<tspan x=\"600\" dy=\"0\">ARTIST</tspan></text><g transform=\"translate(0 218)\">"
    compare = f"{compare}<rect x=\"80\" y=\"0\" width=\"1040\" height=\"634\" "
    compare = f"{compare}rx=\"40\" ry=\"40\" fill=\"#ff0000\" />"
    compare = f"{compare}<g transform=\"translate(0, 317)\">"
    compare = f"{compare}<text y=\"0\" text-anchor=\"middle\" dominant-baseline=\"central\" "
    compare = f"{compare}style=\"font-size:277px;font-style:italic;font-weight:bold;"
    compare = f"{compare}font-family:Noto Serif,Serif;fill:#000000\">"
    compare = f"{compare}<tspan x=\"600\" dy=\"-152\">SOME</tspan>"
    compare = f"{compare}<tspan x=\"600\" dy=\"304\">TITLE</tspan></text></g></g></svg>"
    assert bubble == compare

def test_generate_cross_layout():
    """
    Tests the generate_cross_layout function.
    """
    cross = cg.generate_cross_layout("A Different Title", "New Artists",
            background_color="#ff0101", foreground_color="#eee1e1")
    compare = "<svg viewBox=\"0 0 1200 1600\" xmlns=\"http://www.w3.org/2000/svg\"><defs>"
    compare = f"{compare}<style type=\"text/css\" /></defs>"
    compare = f"{compare}<rect x=\"-1\" y=\"-1\" width=\"1202\" height=\"1602\" fill=\"#ff0101\" />"
    compare = f"{compare}<rect x=\"240\" y=\"-1\" width=\"80\" height=\"1602\" fill=\"#eee1e1\" />"
    compare = f"{compare}<rect x=\"-1\" y=\"380\" width=\"1202\" height=\"80\" fill=\"#eee1e1\" />"
    compare = f"{compare}<text y=\"480\" text-anchor=\"start\" dominant-baseline=\"hanging\" "
    compare = f"{compare}style=\"font-size:148px;font-style:italic;font-weight:bold;"
    compare = f"{compare}font-family:Noto Serif,Serif;fill:#000000\">"
    compare = f"{compare}<tspan x=\"380\" dy=\"0\">A</tspan>"
    compare = f"{compare}<tspan x=\"380\" dy=\"162\">Different</tspan>"
    compare = f"{compare}<tspan x=\"380\" dy=\"162\">Title</tspan></text>"
    compare = f"{compare}<text y=\"300\" text-anchor=\"start\" dominant-baseline=\"alphabetic\" "
    compare = f"{compare}style=\"font-size:127px;font-style:italic;font-weight:bold;"
    compare = f"{compare}font-family:Noto Serif,Serif;fill:#000000\">"
    compare = f"{compare}<tspan x=\"380\" dy=\"0\">Artists</tspan>"
    compare = f"{compare}<tspan x=\"380\" dy=\"-139\">New</tspan></text></svg>"
    assert cross == compare

def test_write_layout_to_image():
    """
    Tests the write_layout_to_image function.
    """
    # Save as a full sized PNG file
    with tempfile.TemporaryDirectory() as temp_dir:
        svg = cg.generate_cross_layout("Something Title!", "Writer",
                background_color="#FF0000", foreground_color="#00FF00")
        image_file = abspath(join(temp_dir, "image.png"))
        assert cg.write_layout_to_image(svg, image_file)
        assert os.listdir(abspath(temp_dir)) == ["image.png"]
        image = Image.open(image_file)
        assert image.size == (1200,1600)
    # Scale and convert to .jpeg
    with tempfile.TemporaryDirectory() as temp_dir:
        image_file = abspath(join(temp_dir, "image.jpeg"))
        assert cg.write_layout_to_image(svg, image_file, width=900)
        assert os.listdir(abspath(temp_dir)) == ["image.jpeg"]
        image = Image.open(image_file)
        assert image.size == (900,1200)

def test_generate_cover():
    """
    Tests the generate_cover function.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        image_file = abspath(join(temp_dir, "image.png"))
        assert cg.generate_cover("Test Title", "Artist", image_file)
        assert os.listdir(temp_dir) == ["image.png"]
        image = Image.open(image_file)
        assert image.size == (1200,1600)
