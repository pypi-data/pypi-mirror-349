#!/usr/bin/env python3

import cover_generator.color as cc

def test_rgb_to_hex():
    """
    Tests the rgb_to_hex function.
    """
    assert cc.rgb_to_hex(1, 0, 0) == "#ff0000"
    assert cc.rgb_to_hex(0, 1, 0) == "#00ff00"
    assert cc.rgb_to_hex(0, 0, 1) == "#0000ff"
    assert cc.rgb_to_hex(0.3333, 0.45, 0.05) == "#54720c"
    assert cc.rgb_to_hex(0.01, 0.02, 0.05) == "#02050c"

def test_get_text_color():
    """
    Tests the get_text_color function.
    """
    assert cc.get_text_color("#ffffff") == "#000000"
    assert cc.get_text_color("#ff0000") == "#000000"
    assert cc.get_text_color("#00aa00") == "#000000"
    assert cc.get_text_color("#000000") == "#ffffff"
    assert cc.get_text_color("#001010") == "#ffffff"

def test_get_all_palettes():
    """
    Tests the get_all_palettes function.
    """
    palettes = cc.get_all_palettes()
    assert len(palettes) == 14
    assert palettes[0]["name"] == "DarkColorContrastAnalogous"
    assert palettes[0]["category"] == "DarkColorContrast"
    assert len(palettes[0]["color_pairs"]) == 14

def test_get_color_pair():
    """
    Tests the get_color_pair function.
    """
    # Test getting color pair from a known palette
    primary, secondary = cc.get_color_pair("Pastel", "PastelTriadic", "2")
    assert primary == "#ffc199"
    assert secondary == "#3d664d"
    # Test getting color pair from a random palette
    primary, secondary = cc.get_color_pair()
    assert not primary == "#ffffff"
    assert not secondary == "#000000"
    # Test getting color pair from an invalid palette
    primary, secondary = cc.get_color_pair("NonExistant", "PastelTriadic", "2")
    assert primary == "#ffffff"
    assert secondary == "#000000"

def test_get_hue_offset():
    """
    Tests the get_hue_offset function.
    """
    # Test normal hue adding
    assert cc.get_hue_offset(0.0,  0.5) == 0.5
    assert cc.get_hue_offset(0.65, 0.2) == 0.85
    # Test if hue is too large
    assert cc.get_hue_offset(0.8, 0.25) == 0.05
    assert cc.get_hue_offset(0.75, 0.5) == 0.25
    assert cc.get_hue_offset(0.5, 5) == 0.5
    # Test if hue is too small
    assert cc.get_hue_offset(0.5, -0.75) == 0.75
    assert cc.get_hue_offset(0.25, -1) == 0.25
    assert cc.get_hue_offset(0.75, -5) == 0.75

def test_generate_offset_palette():
    """
    Tests the generate_offset_palette function.
    """
    # Test generating complimentary palette
    palette = cc.generate_offset_palette("Palette", "Parent", 0.5,
            primary_saturation=1.0, primary_value=0.8,
            secondary_saturation=0.5, secondary_value=0.3)
    assert palette["name"] == "Palette"
    assert palette["category"] == "Parent"
    pairs = palette["color_pairs"]
    assert len(pairs) == 30
    assert pairs[0]["id"] == 0
    assert pairs[0]["primary_color"] == "#cc0000"
    assert pairs[0]["secondary_color"] == "#264c4c"
    assert pairs[29]["id"] == 29
    assert pairs[29]["primary_color"] == "#cc0028"
    assert pairs[29]["secondary_color"] == "#264c44"
    # Test generating triadic palette
    palette = cc.generate_offset_palette("Triadic", "Colors", 0.333,
            primary_saturation=0.8, primary_value=0.9,
            secondary_saturation=0.25, secondary_value=0.9)
    assert palette["name"] == "Triadic"
    assert palette["category"] == "Colors"
    pairs = palette["color_pairs"]
    assert len(pairs) == 30
    assert pairs[0]["id"] == 0
    assert pairs[0]["primary_color"] == "#e52d2d"
    assert pairs[0]["secondary_color"] == "#ace5ac"
    assert pairs[14]["id"] == 14
    assert pairs[14]["primary_color"] == "#2de5c0"
    assert pairs[14]["secondary_color"] == "#d9ace5"
