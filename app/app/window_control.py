from typing import Optional, Tuple, Union

from ahk import AHK
from django.conf import settings

from app.validators import float_or_raise


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

    def send_click(
        self,
        click_position_x_percentage_from_origin: Union[int, float],
        click_position_y_percentage_from_origin: Union[int, float],
    ) -> bool:
        """
        :param click_position_x_percentage_from_origin: X position as percentage from window origin that should be clicked
        :param click_position_y_percentage_from_origin: Y position as percentage from window origin that should be clicked
        :return: True if click was sent to the window
        """
        if self.window:
            self.activate()
            if (
                click_position_x_percentage_from_origin is not None
                and click_position_y_percentage_from_origin is not None
            ):
                click_x, click_y = self._click_window_position(
                    click_position_x_percentage_from_origin,
                    click_position_y_percentage_from_origin,
                )
            settings.LOGGER.warning(
                f"Clicked {click_x}, {click_y} of window {self.window.title}"
            )
            return True
        return False

    def send_drag(
        self,
        from_position_x_percentage_from_origin: Union[int, float],
        from_position_y_percentage_from_origin: Union[int, float],
        to_position_x_percentage_from_origin: Union[int, float],
        to_position_y_percentage_from_origin: Union[int, float],
    ) -> bool:
        """
        Drag mouse over window.

        :param from_position_x_percentage_from_origin: X position as percentage from window origin from where the mouse drag should start
        :param from_position_y_percentage_from_origin: Y position as percentage from window origin from where the mouse drag should start
        :param from_position_x_percentage_from_origin: X position as percentage from window origin to where the mouse drag should end
        :param from_position_y_percentage_from_origin: Y position as percentage from window origin to where the mouse drag should end
        :return: True if mouse drag was sent to the window
        """
        if self.window:
            self.activate()
            if (
                from_position_x_percentage_from_origin is not None
                and from_position_y_percentage_from_origin is not None
                and to_position_x_percentage_from_origin is not None
                and to_position_y_percentage_from_origin is not None
            ):
                from_x, from_y, to_x, to_y = self._drag_mouse_inside_window(
                    from_position_x_percentage_from_origin,
                    from_position_y_percentage_from_origin,
                    to_position_x_percentage_from_origin,
                    to_position_y_percentage_from_origin,
                )
                settings.LOGGER.warning(
                    f"Dragged mouse from {from_x}, {from_y} to {to_x}, {to_y} inside window {self.window.title}"
                )
            return True
        return False

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
        click_position_x_percentage_from_origin: Union[int, float] = 0,
        click_position_y_percentage_from_origin: Union[int, float] = 0,
    ) -> Tuple[Union[int, float], Union[int, float]]:
        """
        Calculate a screen position (x, y) that is going to be clicked.

        :param x: X position of window
        :param y: Y position of window
        :param width: Window width
        :param height: Window height
        :param click_position_x_percentage_from_origin: X position as percentage from window XY origin that should be clicked, defaults to 0
        :param click_position_y_percentage_from_origin: Y position as percentage from window XY origin that should be clicked, defaults to 0
        :return: x, y position in screen to click as tuple
        :raises ValueError: x or y position can't be converted to float or is nan
        """
        return (
            float_or_raise(x + width * click_position_x_percentage_from_origin / 100),
            float_or_raise(
                y + (height - height * click_position_y_percentage_from_origin / 100)
            ),
        )

    def _click_window_position(
        self,
        click_position_x_percentage_from_origin: Union[int, float] = 0,
        click_position_y_percentage_from_origin: Union[int, float] = 0,
    ) -> Tuple[Union[int, float], Union[int, float]]:
        """
        Click a position (x, y from origin) in the window.

        :param click_position_x_percentage_from_origin: X position as percentage from window XY origin that should be clicked, defaults to 0
        :param click_position_y_percentage_from_origin: Y position as percentage from window XY origin that should be clicked, defaults to 0
        :return: x, y position in screen that was clicked as tuple
        """
        click_x, click_y = self._calculate_click_position(
            *self.window.rect,
            click_position_x_percentage_from_origin,
            click_position_y_percentage_from_origin,
        )
        settings.LOGGER.warning(
            f"Moving mouse and clicking to {click_x}, {click_y} inside window {self.window.title}"
        )
        self.autohotkey.click(click_x, click_y, blocking=True)
        return (click_x, click_y)

    def _drag_mouse_inside_window(
        self,
        from_position_x_percentage_from_origin: Union[int, float],
        from_position_y_percentage_from_origin: Union[int, float],
        to_position_x_percentage_from_origin: Union[int, float],
        to_position_y_percentage_from_origin: Union[int, float],
    ) -> Tuple[
        Union[int, float], Union[int, float], Union[int, float], Union[int, float]
    ]:
        """
        Drag mouse over window.

        :param from_position_x_percentage_from_origin: X position as percentage from window origin from where the mouse drag should start
        :param from_position_y_percentage_from_origin: Y position as percentage from window origin from where the mouse drag should start
        :param from_position_x_percentage_from_origin: X position as percentage from window origin to where the mouse drag should end
        :param from_position_y_percentage_from_origin: Y position as percentage from window origin to where the mouse drag should end
        :return: drag position from x, y to x, y as tuple
        """
        rect = self.window.rect
        from_x, from_y = self._calculate_click_position(
            *rect,
            from_position_x_percentage_from_origin,
            from_position_y_percentage_from_origin,
        )
        to_x, to_y = self._calculate_click_position(
            *rect,
            to_position_x_percentage_from_origin,
            to_position_y_percentage_from_origin,
        )

        settings.LOGGER.warning(
            f"Dragging mouse from {from_x}, {from_y} to {to_x}, {to_y} inside window {self.window.title}"
        )
        self.autohotkey.mouse_drag(
            to_x, to_y, from_position=(from_x, from_y), blocking=True
        )
        return (from_x, from_y, to_x, to_y)

    def _send_key(self, command) -> None:
        """
        Send given keys to window.
        """
        self.window.send(command, blocking=True)
