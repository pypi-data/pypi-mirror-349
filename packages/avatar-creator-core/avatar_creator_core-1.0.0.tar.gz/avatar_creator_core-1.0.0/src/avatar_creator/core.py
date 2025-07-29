from PIL import Image
import colorsys

def recolor_to_rgb(
    img: Image.Image,
    target_rgb: tuple[int, int, int]
) -> Image.Image:
    """
    Recolor an RGBA image by applying the hue & saturation of `target_rgb`,
    while preserving the original image’s brightness (value channel).
    Args:
        img (Image.Image): The input image in RGBA mode.
        target_rgb (tuple[int, int, int]): The target RGB color as a tuple of integers (0-255).
    Returns:
        Image.Image: The recolored image in RGBA mode.
    Example:
        ```python
        img = Image.open("input.png").convert("RGBA")
        target_color = (255, 0, 0)  # Red
        recolored_img = recolor_to_rgb(img, target_color)
        recolored_img.save("output.png")
        ```
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Split RGBA and get only V from HSV
    r, g, b, a = img.split()
    _, _, v = Image.merge("RGB", (r, g, b)).convert("HSV").split()

    # Compute target hue & sat in 0–255 scale
    rf, gf, bf = (c / 255.0 for c in target_rgb)
    h_t, s_t, _ = colorsys.rgb_to_hsv(rf, gf, bf)
    h_val = int(h_t * 255)
    s_val = int(s_t * 255)

    # Build new HSV and reattach alpha
    h_chan = Image.new("L", img.size, color=h_val)
    s_chan = Image.new("L", img.size, color=s_val)
    hsv = Image.merge("HSV", (h_chan, s_chan, v))
    rgb = hsv.convert("RGB")
    return Image.merge("RGBA", (*rgb.split(), a))


def load_rgba_image(file_path: str) -> Image.Image:
    """
    Load an image from the given file_path and convert it to RGBA mode.

    Args:
        file_path (str): The path to the image file to load.

    Returns:
        Image.Image: The loaded image in RGBA mode.

    Example:
        ```python
        img = load_rgba_image("avatar.png")
        img.show()
        ```
    """
    return Image.open(file_path).convert("RGBA")

def merge_images(
    base_img: Image.Image,
    *images: Image.Image
) -> Image.Image:
    """
    Merge multiple RGBA images using alpha compositing.
    All images must be the same size.

    Args:
        base_img (Image.Image): The base image to start compositing onto. Must be in RGBA mode.
        *images (Image.Image): One or more images to merge with the base image. Each must be the same size as `base_img` and in RGBA mode.

    Raises:
        ValueError: If no images are provided to merge.
        ValueError: If any image does not match the size of the base image.

    Returns:
        Image.Image: The resulting image after all images have been composited.

    Example:
        img1 = Image.open("base.png").convert("RGBA")
        img2 = Image.open("overlay1.png").convert("RGBA")
        img3 = Image.open("overlay2.png").convert("RGBA")
        result = merge_images(img1, img2, img3)
        result.save("merged.png")
    """
    if not images:
        raise ValueError("At least one image must be provided.")
    for img in images:
        if img.size != base_img.size:
            raise ValueError("All images must be the same size.")
        base_img = Image.alpha_composite(base_img, img)
    return base_img