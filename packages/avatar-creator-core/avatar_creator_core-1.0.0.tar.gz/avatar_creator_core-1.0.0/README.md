# Avatar Creator Core

[![Build and Test Python Package](https://github.com/Darker21/avatar-creator-core/actions/workflows/build-and-test.yml/badge.svg?branch=develop)](https://github.com/Darker21/avatar-creator-core/actions/workflows/build-and-test.yml)

[![codecov](https://codecov.io/gh/Darker21/avatar-creator-core/graph/badge.svg?token=HT31UAR4AY)](https://codecov.io/gh/Darker21/avatar-creator-core)

A Python library for recoloring white-hair assets and compositing avatar images using Pillow.

## Features

- Recolor hair images to any RGB color while preserving shading.
- Composite hair and face images to create custom avatars.
- Simple API for loading, recoloring, and merging images.

## Installation

```sh
pip install pillow
```

Or install from source:

```sh
pip install .
```

## Usage

Example script ([cli/main.py](cli/main.py)):

```python
import os
import avatar_creator.core as core

hair_file = os.path.join("content/hair", "mid-length.png")
face_file = os.path.join("content/face", "face_1.png")

# Load images
face_img = core.load_rgba_image(face_file)
hair_img = core.load_rgba_image(hair_file)

# Recolor hair to orange
hair_img = core.recolor_to_rgb(hair_img, (255, 144, 25))

# Composite hair over face
avatar = core.merge_images(face_img, hair_img)

# Save result
avatar.save("output.png")
```

### Example: Creating a blue-haired avatar

```python
import os
import avatar_creator.core as core

face_img = core.load_rgba_image(
    os.path.join("content/face", "face_2.png")
)
hair_img = core.load_rgba_image(
    os.path.join("content/hair", "short.png")
)
hair_img = core.recolor_to_rgb(hair_img, (50, 100, 255))  # Blue
avatar = core.merge_images(face_img, hair_img)
avatar.save("avatar-blue.png")
```

### Example: Batch generate avatars with different hair colors

```python
import os
import avatar_creator.core as core

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue
face_img = core.load_rgba_image(
    os.path.join("content/face", "face_1.png")
)
hair_img = core.load_rgba_image(
    os.path.join("content/hair", "mid-length.png")
)

for color in colors:
    recolored = core.recolor_to_rgb(hair_img, color)
    avatar = core.merge_images(face_img, recolored)
    avatar.save(f"avatar-{color[0]}-{color[1]}-{color[2]}.png")
```

---

## Example Images

| Face Example                | Hair Example                | Resulting Avatar Example         |
|----------------------------|-----------------------------|----------------------------------|
| ![face_1.png](docs/example/face.png) | ![mid-length.png](docs/example/hair.png) | ![output.png](docs/example/output.png)        |

If running the [`cli/main.py`]("/cli/main.py") Place your face and hair images in the `cli/content/face/` and `cli/content/hair/` folders, respectively.

---

## API

### [`avatar_creator.core.recolor_to_rgb`](src/avatar_creator/core.py)

```python
recolor_to_rgb(img: Image.Image, target_rgb: tuple[int, int, int]) -> Image.Image
```
Recolors an RGBA image to the target RGB color, preserving the original brightness.

### [`avatar_creator.core.load_rgba_image`](src/avatar_creator/core.py)

```python
load_rgba_image(file_path_: str) -> Image.Image
```
Loads an image from a directory and converts it to RGBA.

### [`avatar_creator.core.merge_images`](src/avatar_creator/core.py)

```python
merge_images(base_img: Image.Image, *images: Image.Image) -> Image.Image
```
Alpha-composites multiple RGBA images. All images must be the same size.

## License

MIT License. See [LICENSE](LICENSE).