# FindaCat API Wrapper

A lightweight Python wrapper for the [finda.cat](https://finda.cat) API, providing easy access to cat images and related data.

## Features

- Get random cat images with customizable options (format, blur, saturation, text, etc.)
- Retrieve API statistics
- Get all available cat image IDs
- Access the history of cat images in Base64 format

## Installation

- Python 3.7 or higher

```bash
pip install findacat
```

## Usage

```python
from findacat import FindaCat, CatOptions

client = FindaCat()
opts = CatOptions(format="png", blur=1)

# Get a random cat image with options
image_bytes = client.get_cat_image(opts)

with open("cat.png", "wb") as f:
    f.write(image_bytes)

# Get API statistics (JSON)
stats = client.get_stats()
print(stats)

# Get all cat image IDs (JSON)
all_images = client.get_all_images()
print(all_images)

# Get Base64 cat images history (JSON)
history = client.get_history()
print(history)
```

## Notes

- The get_cat_image method returns the image content as bytes.
- Other methods return JSON responses from the API.
- Use CatOptions to customize the image request parameters.
- Errors from the API are raised as exceptions for image requests, or returned as JSON with an "error" key for data requests.

## Links

- [finda.cat](https://finda.cat)
- [Discord](https://discord.gg/undesync)
