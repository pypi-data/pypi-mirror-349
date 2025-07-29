#!/usr/bin/env python3

import cover_generator.font_handling as fh
from os.path import abspath, join

def test_get_glyph_sizes():
    """
    Tests the get_glyph_sizes function.
    """
    # Test getting sizes from JSON file
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-Bold.json")
    assert glyph_sizes["A"] == {"width":0.854, "height":0.82}
    assert glyph_sizes["W"] == {"width":1.167, "height":0.82}
    assert glyph_sizes["widest"] == {"width":1.167, "height":0.82}
    # Test getting sizes from font file
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-BoldItalic.ttf")
    assert glyph_sizes["A"] == {"width":0.858, "height":0.82}
    assert glyph_sizes["W"] == {"width":1.177, "height":0.82}
    assert glyph_sizes["widest"] == {"width":1.177, "height":0.82}
    # Test getting sizes from name with no extension
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-Bold")
    assert glyph_sizes["A"] == {"width":0.854, "height":0.82}
    assert glyph_sizes["W"] == {"width":1.167, "height":0.82}
    assert glyph_sizes["widest"] == {"width":1.167, "height":0.82}

def test_get_string_size():
    """
    Tests the get_string_size function.
    """
    # Check a standard string
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-Bold.ttf")
    assert fh.get_string_size("Just a test.", glyph_sizes) == (6.442, 1.06)
    # Check a string with narrow characters
    assert fh.get_string_size("IIIIIIIIII", glyph_sizes) == (5.01, 0.82)
    # Check a string with wide characters
    assert fh.get_string_size("WWWWWWWWWW", glyph_sizes) == (11.67, 0.82)
    # Check with unseen character
    assert fh.get_string_size("AAA—AAA", glyph_sizes) == (6.291, 1.11)

def test_get_largest_line_size():
    """
    Tests the get_largest_line_size function.
    """
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-Bold.ttf")
    assert fh.get_largest_line_size(["aa", "WWW", "IIIII"], glyph_sizes) == (3.501, 0.82)
    assert fh.get_largest_line_size(["a"], glyph_sizes) == (0.699, 0.66)

def test_word_wrap():
    """
    Tests the word_wrap function.
    """
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-Bold.ttf")
    assert fh.word_wrap("A list of words!!!", glyph_sizes, 4) == ["A list", "of", "words!!!"]
    assert fh.word_wrap("III WWWW IIIII WW", glyph_sizes, 6) == ["III", "WWWW", "IIIII WW"]

def test_max_word_wrap():
    """
    Tests the max_word_wrap function.
    """
    # Test word wrapping with default limit
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-Bold.ttf")
    text = "These are words."
    assert fh.max_word_wrap(text, glyph_sizes) == ["These", "are", "words."]
    text = "  This \nis  significantly longer.  "
    assert fh.max_word_wrap(text, glyph_sizes) == ["This is", "significantly", "longer."]
    # Test word wrapping when no words exceed the minimum width limit
    text = "3 tiny words"
    assert fh.max_word_wrap(text, glyph_sizes, 5) == ["3 tiny", "words"]
    # Test that maximum number of lines are not exceeded
    text = "Long list of small words."
    assert fh.max_word_wrap(text, glyph_sizes, 3, max_lines=3) == ["Long list", "of small", "words."]
    assert fh.max_word_wrap(text, glyph_sizes, 3, max_lines=4) == ["Long", "list of", "small", "words."]
    assert fh.max_word_wrap(text, glyph_sizes, 3, max_lines=20) == ["Long", "list of", "small", "words."]
    # Test line breaks made after colon
    text = "One: To Three"
    assert fh.max_word_wrap(text, glyph_sizes, 15) == ["One:", "To Three"]
    text = "A Long Phrase: A Small Title"
    assert fh.max_word_wrap(text, glyph_sizes, 5) == ["A Long", "Phrase:", "A Small Title"]
    
def test_get_optimized_line_number():
    """
    Tests the get_optimized_line_number function.
    """
    # Test with short text
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-Bold.ttf")
    assert fh.get_optimized_line_number("A", glyph_sizes) == 3
    assert fh.get_optimized_line_number("A Short Title", glyph_sizes) == 3
    # Test with longer text
    text = "THIS STRING IS HONESTLY FAR TOO LONG FOR A TITLE"
    assert fh.get_optimized_line_number(text, glyph_sizes) == 5
    # Test with very long text
    assert fh.get_optimized_line_number("A"*200, glyph_sizes) == 6

def test_get_text_size():
    """
    Tests the get_text_size function.
    """
    # Test limiting size by number of lines
    glyph_sizes = fh.get_glyph_sizes("NotoSerif-Bold.ttf")
    lines = ["single line"]
    assert fh.get_text_size(lines, glyph_sizes, 7000, 100, height_multiplier=1.2) == 100
    lines = ["these", "are", "lines"]
    assert fh.get_text_size(lines, glyph_sizes, 7000, 300, height_multiplier=1.2) == 83
    lines = ["these", "are", "more", "lines"]
    assert fh.get_text_size(lines, glyph_sizes, 7000, 300, height_multiplier=1.2) == 62
    # Test limiting size by length of the longest line
    lines = ["1234567890"]
    assert fh.get_text_size(lines, glyph_sizes, 300, 7000) == 45
    lines = ["small", "Much Larger Line", "small"]
    assert fh.get_text_size(lines, glyph_sizes, 200, 7000) == 18
