from logging import getLogger
import os
from tempfile import TemporaryDirectory
import time

import click
import requests
from tracker.config import APISettings
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


SIZE_CONFIG = {
    ImageType.backdrop: {
        "widths": {
            "small": 576,
            "medium": 1280,
            "large": 1920,
        },
        "ratio": (16, 9),
    },
    ImageType.poster: {
        "widths": {
            "small": 360,
            "medium": 720,
            "large": 1080,
        },
        "ratio": (9, 16),
    },
}


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
        # TODO(milo): Refactor this to use constant
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
        all_local_paths = [
            image.local_small(self.local_dir),
            image.local_medium(self.local_dir),
            image.local_large(self.local_dir),
        ]
        if all(os.path.exists(path) for path in all_local_paths):
            logger.info("all images already exists locally")
            return

        # hacky way to make sure I am not overloading the api they have
        if self.db.current_request_count >= self.db.max_requests_per_second:
            logger.debug("Gotta chill for a second")
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
        sm_path = image.local_small(self.local_dir)
        logger.debug(f"working on image for path {sm_path}")
        os.makedirs(os.path.dirname(sm_path), exist_ok=True)
        # resize and store the images locally
        resize_image(
            temp_path,
            self.config[image.image_type]["widths"]["small"],
            sm_path,
        )
        md_path = image.local_medium(self.local_dir)
        logger.debug(f"working on image for path {md_path}")
        os.makedirs(os.path.dirname(md_path), exist_ok=True)
        resize_image(
            temp_path,
            self.config[image.image_type]["widths"]["medium"],
            md_path,
        )
        lg_path = image.local_large(self.local_dir)
        logger.debug(f"working on image for path {lg_path}")
        os.makedirs(os.path.dirname(lg_path), exist_ok=True)
        resize_image(
            temp_path,
            self.config[image.image_type]["widths"]["large"],
            lg_path,
        )


@click.command()
@click.option(
    "--image",
    "-i",
    help="path to image",
    type=click.Path(exists=True, readable=True, dir_okay=False),
    required=True,
)
@click.option(
    "--kind",
    "-k",
    help="kind of image",
    type=click.Choice(ImageType),
    required=True,
)
@click.option(
    "--id",
    help="id of image",
    type=click.INT,
    default=0,
)
def main(
    image: str,
    kind: ImageType,
    id: int = 0,
):
    config = APISettings()
    with TemporaryDirectory() as temp_dir:
        image_downloader = ImageDownloader(
            TVMovieDB(),
            config.local_files_dir,
        )

        image_downloader._store_image(
            image,
            Image(
                show_id=id,
                image_type=kind,
            ),
            temp_dir,
        )
    click.echo("Saved images")


if __name__ == "__main__":
    main()
