#!/usr/bin/env python3

import math
from pathlib import Path

from PIL import Image
import pytweening

def adjust_exposure_gimp_style(image: Image.Image, exposure: float) -> Image.Image:
    """
    Adjust image exposure using GIMP-style logarithmic transformation.

    Args:
        image: PIL Image object
        exposure: Exposure value (-5.0 to 5.0, where 0.0 is normal)

    Returns:
        PIL Image object with adjusted exposure
    """
    # Convert to linear RGB space first
    rgb = image.convert('RGB')
    r, g, b = rgb.split()

    # Apply logarithmic transformation
    def log_transform(pixel):
        # Convert to logarithmic scale
        log_val = math.log1p(pixel) / math.log(256)
        # Apply exposure adjustment
        adjusted = log_val * (1 + exposure/5.0)
        # Convert back to linear scale
        return min(255, max(0, round(math.exp(adjusted * math.log(256)) - 1)))

    # Apply transformation to each channel
    r_adj = Image.frombytes('L', r.size, bytes([log_transform(p) for p in r.tobytes()]))
    g_adj = Image.frombytes('L', g.size, bytes([log_transform(p) for p in g.tobytes()]))
    b_adj = Image.frombytes('L', b.size, bytes([log_transform(p) for p in b.tobytes()]))

    return Image.merge('RGB', (r_adj, g_adj, b_adj))

def adjust_levels(image: Image.Image, from_value: int) -> Image.Image:
    """
    Adjust image levels to map values from [0,255] to [from_value,255].

    Args:
        image: PIL Image object

    Returns:
        PIL Image object with adjusted levels
    """
    # Convert to RGB mode first
    rgb = image.convert('RGB')
    r, g, b = rgb.split()

    def levels_transform(pixel):
        # Linear mapping from [0,255] to [from_value,255]
        return from_value + (pixel * (255 - from_value)) // 256

    # Apply transformation to each channel
    r_adj = Image.frombytes('L', r.size, bytes([levels_transform(p) for p in r.tobytes()]))
    g_adj = Image.frombytes('L', g.size, bytes([levels_transform(p) for p in g.tobytes()]))
    b_adj = Image.frombytes('L', b.size, bytes([levels_transform(p) for p in b.tobytes()]))

    return Image.merge('RGB', (r_adj, g_adj, b_adj))

def fade_with_exposure(input_path: Path, output_path: Path, cropped_dir: Path, exposure: float, level: int, opacity: float):
    """
    Fade out an image by combining two versions of an image:
    one levelled and exposed, and one faded, using opacity for blending.

    Args:
        input_path (str): Path to the input JPG image
        output_path (str): Path where the output JPG will be saved
        exposure_value (float): Exposure adjustment (-5.0 to 5.0)
        opacity (float): Opacity of the top layer (0.0 to 1.0)
    """
    # Validate input parameters
    if not -5 <= exposure <= 5:
        raise ValueError("Exposure value must be between -5.0 and 5.0")
    if not 0 <= opacity <= 1:
        raise ValueError("Opacity must be between 0 and 1")

    # Check if input file exists
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Open and convert image
    with Image.open(input_path) as img:
        # (1) Expose the original
        # Create exposed version using GIMP-style exposure
        exposed = adjust_exposure_gimp_style(img, exposure)

        # (2) Map the exposed to a value level
        exposed_levelled = adjust_levels(exposed, level)
        exposed_levelled_rgba = exposed_levelled.convert('RGBA')

        # (3) Fade the original with opacity to white
        # Adjust opacity using split/merge operations
        rgba_img = img.convert('RGBA')
        r, g, b, a = rgba_img.split()
        a = Image.blend(a, Image.new('L', img.size, int(255 * opacity)), 1)
        faded_rgba = Image.merge('RGBA', (r, g, b, a))

        # Combine layers
        combined = Image.alpha_composite(exposed_levelled_rgba, faded_rgba).convert('RGB')

        # Save result.
        # Default is quality=75, moonstone-1.jpg 414.3 KiB, main.pdf 18.9 MiB
        #            quality=85, moonstone-1.jpg 547.0 KiB, main.pdf 22.4 MiB
        # 3.5 MB difference
        combined.save(output_path, optimize=True, quality=85)

        # Save a cropped version for the epub
        cropped_output_path = cropped_dir.joinpath(output_path.stem + "-crop" + ".jpg")
        cropped = combined.crop(
            (
                135,  # Left X
                615,  # Upper Y
                1864,  # Right X
                1333,  # Lower Y
            )
        )

        new_width = 500
        aspect_ratio = cropped.height / cropped.width
        new_height = int(new_width * aspect_ratio)
        resized = cropped.resize((new_width, new_height), Image.Resampling.LANCZOS)

        resized.save(cropped_output_path, optimize=True, quality=85)

if __name__ == "__main__":
    input_path = Path(__file__).parent.joinpath("moonstone-polonnaruwa-bw.jpg")

    # Chapter 33 has white bg
    # Range is up to 32
    last = 33
    for i in range(1, last):
        # 01: 0.00, 190, 0.00
        # ...
        # 32: 2.50, 230, 0.05

        # See tweening function charts:
        # https://github.com/asweigart/pytweening

        p = i / (last-1) # convert to 0.0 - 1.0
        x = pytweening.easeInCubic(p) * last

        exposure = 0.0 + x*(2.5/last)
        level = int(190 + x*((230-190)/last))
        opacity = 0.0 + x*(0.05/last)

        # print(f"{i} {x:.2f} {p:.2f}")
        print(f"{i:02}: {exposure:.2f}, {level}, {opacity:.2f}")

        output_path = Path(f"./assets/images/moonstone-{i}.jpg")
        cropped_dir = Path("./manuscript/markdown/assets/images/")
        fade_with_exposure(input_path, output_path, cropped_dir, exposure, level, opacity)
