from logging import getLogger
import os
from tempfile import TemporaryDirectory
import time

import requests
from tracker.query.model import Image, ImageType
from .base import TVMovieDB
from PIL import Image as PILImage


logger = getLogger(__name__)


def scale_to_ratio(
    image_path: str,
    output_path: str,
    aspect_width: int = 16,
    aspect_height: int = 9,
):
    """
    Scales an image to a specific aspect ratio, adding black bars if necessary.

    Args:
        image_path: Path to the input image.
        output_path: Path to save the scaled image.
        aspect_width: Width of the target aspect ratio.
        aspect_height: Height of the target aspect ratio.
    """
    img = PILImage.open(image_path)
    width, height = img.size
    target_aspect = aspect_width / aspect_height
    image_aspect = width / height

    if image_aspect == target_aspect:
        # Image is already 16:9, no scaling needed
        img.save(output_path)
        return

    if image_aspect > target_aspect:
        # Image is wider than 16:9, scale to fit height, add black bars to sides
        new_width = int(height * target_aspect)
        resized_img = img.resize((new_width, height), PILImage.Resampling.LANCZOS)

        # Create a new image with black background and paste the resized image
        new_img = PILImage.new("RGB", (int(width), height), "black")
        new_img.paste(resized_img, ((width - new_width) // 2, 0))
        new_img.save(output_path)

    else:
        # Image is taller than 16:9, scale to fit width, add black bars to top/bottom
        new_height = int(width / target_aspect)
        resized_img = img.resize((width, new_height), PILImage.Resampling.LANCZOS)

        # Create a new image with black background and paste the resized image
        new_img = PILImage.new("RGB", (width, int(height)), "black")
        new_img.paste(resized_img, (0, (height - new_height) // 2))
        new_img.save(output_path)


def resize_image(image_path, new_width, output_path):
    image = PILImage.open(image_path)
    width, height = image.size
    new_height = int(height * (new_width / width))
    resized_image = image.resize((new_width, new_height))
    resized_image.save(output_path)
    logger.debug(f"Saved image to path: {output_path}")


class ImageDownloader:
    def __init__(
        self,
        db: TVMovieDB,
        local_dir: str,
    ) -> None:
        logger.debug(f"initializing image downloader at {local_dir}")
        self.db = db
        self.local_dir = os.path.normpath(local_dir)
        value = db.request("/configuration", params={"language": "en-US"})
        images = value["images"]

        self.base_url = images["base_url"]
        self.config = {
            ImageType.backdrop: {
                "size": images["backdrop_sizes"][-1],
                "ratio": (16, 9),
                "widths": {
                    "small": 576,
                    "medium": 1280,
                    "large": 1920,
                },
            },
            ImageType.poster: {
                "size": images["poster_sizes"][-1],
                "ratio": (9, 16),
                "widths": {
                    "small": 360,
                    "medium": 720,
                    "large": 1080,
                },
            },
        }

    def download(self, image: Image, path: str) -> None:
        logger.info(f"downloading image, {image} from path {path}")
        # hacky way to make sure I am not overloading the api they have
        if self.db.current_request_count >= self.db.max_requests_per_second:
            self.db.current_request_count = 0
            time.sleep(1)
        self.db.current_request_count += 1

        with TemporaryDirectory() as temp_path:
            image_path = (
                f"{self.base_url}/{self.config[image.image_type]['size']}{path}"
            )
            response = requests.get(image_path, stream=True)
            response.raise_for_status()

            local_image_path = os.path.join(temp_path, "temp_image.png")
            with open(local_image_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self._store_image(local_image_path, image, temp_path)

    def _store_image(self, image_path: str, image: Image, temp_path: str):
        temp_path = f"{temp_path}/sized_temp_image.png"
        logger.debug(f"working on image {temp_path}")
        # ensure image is expected ratio for its type
        scale_to_ratio(image_path, temp_path, *self.config[image.image_type]["ratio"])
        sm_path = os.path.join(self.local_dir, image.small.lstrip("/"))
        logger.debug(f"working on image for path {sm_path}")
        os.makedirs(os.path.dirname(sm_path), exist_ok=True)
        # resize and store the images locally
        resize_image(
            temp_path,
            self.config[image.image_type]["widths"]["small"],
            sm_path,
        )
        md_path = os.path.join(self.local_dir, image.medium.lstrip("/"))
        logger.debug(f"working on image for path {md_path}")
        os.makedirs(os.path.dirname(md_path), exist_ok=True)
        resize_image(
            temp_path,
            self.config[image.image_type]["widths"]["medium"],
            md_path,
        )
        lg_path = os.path.join(self.local_dir, image.large.lstrip("/"))
        logger.debug(f"working on image for path {lg_path}")
        os.makedirs(os.path.dirname(lg_path), exist_ok=True)
        resize_image(
            temp_path,
            self.config[image.image_type]["widths"]["large"],
            lg_path,
        )
