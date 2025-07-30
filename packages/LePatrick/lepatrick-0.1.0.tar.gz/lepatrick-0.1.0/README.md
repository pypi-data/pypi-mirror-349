# LePatrick

Augment your images with Patrick Star!  
LePatrick is a Python package that applies fun and creative Patrick imprints to images using OpenCV.

---

### What It Does

LePatrick enhances images by pasting Patrick Star's figure onto your input image — great for data augmentation, or just plain fun.

### Features

- Add Patrick imprints with a single function
- Uses OpenCV and NumPy for high-performance image processing
- Installable via PyPI

---

## Installation

Install from [PyPI](https://pypi.org/project/LePatrick):

```bash
pip install LePatrick
```

## Example Usage
```python
import cv2
from LePatrick import Patrick

# Apply to your dataset
Patrick(
    source_dir = "data/train",
    num_outputs = 1000,
    num_patricks = 5
)
```

> [!NOTE]
> The `patrick.png` asset is bundled within the package and loaded internally.

## Requirements

- Python 3.10 or newer
- OpenCV 4.9.0.80
- NumPy 1.26.4

These are installed automatically when you install the package.
