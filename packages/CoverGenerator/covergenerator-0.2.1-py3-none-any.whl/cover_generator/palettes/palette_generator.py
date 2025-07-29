import os
import json
import cover_generator.color as cc
import cover_generator.cover_generator as cg
from os.path import abspath, exists, join

def user_generate_palettes():
    """
    Generates palette and example images for each color pair in the palette.
    """
    hue_offset = None
    primary_saturation = None
    primary_value = None
    secondary_saturation = None
    secondary_value = None
    # Get values from the user
    palette_category = input("Palette Category: ")
    palette_name = input("Palette Name: ")
    while hue_offset is None:
        try:
            hue_offset = float(1 / int(input("Hue Offset (1/X): ")))
        except ValueError: hue_offset = None
    while primary_saturation is None:
        try:
            primary_saturation = float(input("Primary Saturation (0.0 - 1.0): "))
        except ValueError: primary_saturation = None
    while primary_value is None:
        try:
            primary_value = float(input("Primary Value (0.0 - 1.0): "))
        except ValueError: primary_value = None
    while secondary_saturation is None:
        try:
            secondary_saturation = float(input("Secondary Saturation (0.0 - 1.0): "))
        except ValueError: secondary_saturation = None
    while secondary_value is None:
        try:
            secondary_value = float(input("Secondary Value (0.0 - 1.0): "))
        except ValueError: secondary_value = None
    # Generate the user offset Palette
    palette = cc.generate_offset_palette(palette_name, palette_category, hue_offset,
            primary_saturation=primary_saturation, primary_value=primary_value,
            secondary_saturation=secondary_saturation, secondary_value=secondary_value)
    # Run through all pairs in the palette
    base_directory = abspath(os.getcwd())
    palette_directory = abspath(join(base_directory, palette_name))
    if not exists(palette_directory):
        os.mkdir(palette_directory)
    for pair in palette["color_pairs"]:
        identifier = str(pair['id']).zfill(2)
        # Write border layout
        cover_image = abspath(join(palette_directory, f"[{identifier}] {palette_name} (border).png"))
        svg = cg.generate_border_layout("Palette Tester", "Author", pair["primary_color"], pair["secondary_color"])
        cg.write_layout_to_image(svg, cover_image)
        # Write bubble layout
        cover_image = abspath(join(palette_directory, f"[{identifier}] {palette_name} (bubble).png"))
        svg = cg.generate_bubble_layout("Palette Tester", "Author", pair["primary_color"], pair["secondary_color"])
        cg.write_layout_to_image(svg, cover_image)
        # Save Cover Image
        print(f"{palette_name} ({identifier})")
    # Save palette as a json file
    palette_file = abspath(join(palette_directory, f"{palette_name}.json"))
    with open(palette_file, "w", encoding="UTF-8") as out_file:
        out_file.write(json.dumps(palette, indent="   ", separators=(", ", ": ")))

if __name__ == "__main__":
    user_generate_palettes()