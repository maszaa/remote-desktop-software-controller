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

    def send_key(self, command: str, window_needs_clicking: bool = False) -> None:
        """
        Send given command (keys)

        :param command: keys to send
        :param window_needs_clicking: click the window after activating it and before sending keys
        """
        if self.window:
            self.activate()
            if window_needs_clicking is True:
                self._click_window_center()
            self._send_key(command)
            settings.LOGGER.warning(f"Sent {command} to window {self.window.title}")

    def _click_window_center(self) -> None:
        """
        Click the center of the window.
        """
        x, y, width, height = self.window.rect
        click_x, click_y = x + width / 2, y + height / 2
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
