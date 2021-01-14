from typing import Optional, Tuple

from ahk import AHK
from django.conf import settings


class WindowControl:
    def __init__(self, window_title: str) -> "WindowControl":
        self.autohotkey = AHK()
        self.window = self.autohotkey.find_window(title=window_title.encode("utf-8"))

        if not self.window:
            settings.LOGGER.error(f"Window {window_title} not found")

    def activate(self) -> None:
        """
        Activate window i.e. bring it to front.
        """
        if self.window:
            self.window.activate()

    def send_key(
        self,
        command: str,
        click_position_x_percentage_from_origin: int,
        click_position_y_percentage_from_origin: int,
    ) -> bool:
        """
        Send given command (keys)

        :param command: keys to send
        :param click_position_x_percentage_from_origin: X position as percentage from window origin that should be clicked
        :param click_position_y_percentage_from_origin: Y position as percentage from window origin that should be clicked
        :return: True if keys were sent to the window
        """
        if self.window:
            self.activate()
            if (
                click_position_x_percentage_from_origin is not None
                and click_position_y_percentage_from_origin is not None
            ):
                self._click_window_position(
                    click_position_x_percentage_from_origin,
                    click_position_y_percentage_from_origin,
                )
            self._send_key(command)
            settings.LOGGER.warning(f"Sent {command} to window {self.window.title}")
            return True
        return False

    def _calculate_click_position(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        click_position_x_percentage_from_origin: int = 0,
        click_position_y_percentage_from_origin: int = 0,
    ) -> Tuple[int, int]:
        """
        Calculate a screen position (x, y) that is going to be clicked.

        :param x: X position of window
        :param y: Y position of window
        :param width: Window width
        :param height: Window height
        :param click_position_x_percentage_from_origin: X position as percentage from window XY origin that should be clicked, defaults to 0
        :param click_position_y_percentage_from_origin: Y position as percentage from window XY origin that should be clicked, defaults to 0
        :return: x, y position in screen to click as tuple
        """
        return (
            x + width * click_position_x_percentage_from_origin / 100,
            y + (height - height * click_position_y_percentage_from_origin / 100),
        )

    def _click_window_position(
        self,
        click_position_x_percentage_from_origin: int = 0,
        click_position_y_percentage_from_origin: int = 0,
    ) -> None:
        """
        Click a position (x, y from origin) in the window.

        :param click_position_x_percentage_from_origin: X position as percentage from window XY origin that should be clicked, defaults to 0
        :param click_position_y_percentage_from_origin: Y position as percentage from window XY origin that should be clicked, defaults to 0
        """
        click_x, click_y = self._calculate_click_position(
            *self.window.rect,
            click_position_x_percentage_from_origin,
            click_position_y_percentage_from_origin,
        )
        settings.LOGGER.warning(
            f"Window {self.window.title} requires clicking it before sending keys. "
            f"Moving mouse and clicking to {click_x}, {click_y}"
        )
        self.autohotkey.click(click_x, click_y)

    def _send_key(self, command) -> None:
        """
        Send given keys to window.
        """
        self.window.send(command, blocking=True)
