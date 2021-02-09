import io
from typing import Optional

import pyautogui
from django.conf import settings
from PIL import Image

from app.window_control import WindowControl


class Screenshot:
    def __init__(self, window_title: str) -> "Screenshot":
        self.window_title = window_title
        self.window_control = WindowControl(window_title)

    def capture(self) -> Optional[bytes]:
        """
        Capture screenshot from window and return the image as bytes

        :return: screenshot image as bytes if screenshot was captured
        """
        if self.window_control.exists:
            self.window_control.activate()

            image = pyautogui.screenshot(region=self.window_control.size_and_position)

            if not image:
                return None

            settings.LOGGER.warning(
                f"Captured screenshot of window {self.window_title}"
            )
            return self._get_binary_data(image)

    def _get_binary_data(self, image: Image) -> bytes:
        """
        Convert image to binary data

        :param image: Image as PIL.Image
        :return: Image as binary data
        """
        output = io.BytesIO()
        image.save(output, format=settings.SCREENSHOT_IMAGE_FORMAT)
        return output.getvalue()
