from PIL import Image
import pytest
from avatar_creator.core import recolor_to_rgb, load_rgba_image, merge_images

def create_test_image(color=(255, 255, 255, 255), size=(4, 4)):
    img = Image.new("RGBA", size, color)
    return img

def test_recolor_to_rgb_changes_hue_and_saturation():
    img = create_test_image((255, 255, 255, 255))
    target_rgb = (255, 0, 0)  # Red
    recolored = recolor_to_rgb(img, target_rgb)
    assert recolored.mode == "RGBA"
    # All pixels should be red with original alpha
    for pixel in recolored.getdata():
        r, g, b, a = pixel
        assert r > 200 and g < 60 and b < 60 and a == 255

def test_recolor_to_rgb_preserves_brightness():
    img = create_test_image((128, 128, 128, 255))
    target_rgb = (0, 255, 0)  # Green
    recolored = recolor_to_rgb(img, target_rgb)
    # Should not be pure green, but greenish with same brightness
    for pixel in recolored.getdata():
        r, g, b, a = pixel
        assert g > r and g > b and a == 255

def test_load_rgba_image_loads_and_converts(tmp_path):
    # Create a test image and save as PNG
    img = create_test_image((10, 20, 30, 40))
    test_dir = tmp_path
    test_file = test_dir / "test.png"
    img.save(test_file)
    loaded = load_rgba_image(test_file)
    assert loaded.mode == "RGBA"
    assert loaded.size == img.size
    assert list(loaded.getdata())[0] == (10, 20, 30, 40)

def test_merge_images_merges_two_images():
    base = create_test_image((255, 0, 0, 255))
    overlay = create_test_image((0, 255, 0, 128))
    merged = merge_images(base.copy(), overlay)
    assert merged.mode == "RGBA"
    # Check that the merged image is not identical to base or overlay
    assert list(merged.getdata())[0] != (255, 0, 0, 255)
    assert list(merged.getdata())[0] != (0, 255, 0, 128)

def test_merge_images_raises_on_size_mismatch():
    base = create_test_image((255, 0, 0, 255), (4, 4))
    overlay = create_test_image((0, 255, 0, 128), (2, 2))
    with pytest.raises(ValueError):
        merge_images(base, overlay)

def test_merge_images_raises_on_no_images():
    base = create_test_image()
    with pytest.raises(ValueError):
        merge_images(base)