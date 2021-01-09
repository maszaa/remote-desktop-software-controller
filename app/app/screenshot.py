import io
import logging

import pyautogui
import win32gui
from django.conf import settings
from PIL import Image

from app.window_control import WindowControl


class Screenshot:
    def __init__(self, window_title: str) -> "Screenshot":
        self.window_title = window_title
        self.window_control = WindowControl(window_title)

    def capture(self) -> bytes:
        """
        Capture screenshot from window and return the image as bytes

        :return: screenshot image as bytes
        """
        self.window_control.activate()
        hwnd = win32gui.FindWindow(None, self.window_title)

        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            image = pyautogui.screenshot(region=(x, y, x1, y1))

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
