from django.db import models

from app.models.command_group import CommandGroup
from app.models.key import Key
from app.validators import CLICK_POSITION_PERCENTAGE_VALIDATOR


class Command(models.Model):
    name = models.TextField(blank=False)
    order = models.PositiveIntegerField(default=0)
    command_group = models.ForeignKey(
        CommandGroup, on_delete=models.CASCADE, related_name="commands"
    )
    key = models.ForeignKey(Key, blank=True, null=True, on_delete=models.RESTRICT)
    multiplier = models.PositiveIntegerField(default=1)
    free_text = models.TextField(blank=True)
    override_click_position_x_percentage_from_origin = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Override X position as percentage from window origin that should be clicked before sending command",
        validators=(CLICK_POSITION_PERCENTAGE_VALIDATOR,),
    )
    override_click_position_y_percentage_from_origin = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Override Y position as percentage from window origin that should be clicked before sending command",
        validators=(CLICK_POSITION_PERCENTAGE_VALIDATOR,),
    )

    class Meta:
        ordering = ["command_group__order", "command_group__name", "order", "name"]

    def __str__(self) -> str:
        command = (
            self.__class__.objects.filter(pk=self.pk)
            .select_related("command_group__window__software")
            .first()
        )
        software = command.command_group.window.software.name
        window = command.command_group.window.title
        command_group = command.command_group.name

        return f"{software}: {window} - {command_group}: {self.order}. {self.name} ( '{self.command}' )"

    @property
    def command(self) -> str:
        """
        Render the command.

        :return: str
        """
        if self.key:
            return "".join(self.key.key for i in range(self.multiplier))
        return self.free_text

    @property
    def click_position_x_percentage_from_origin(self) -> int:
        """
        Get X position as percentage from window origin that should be clicked before sending command.
        Return override if exists.
        If not, get position from command_group.window.

        :return: X position as percentage to click.
        """
        if self.override_click_position_x_percentage_from_origin is not None:
            return self.override_click_position_x_percentage_from_origin
        return self.command_group.window.click_position_x_percentage_from_origin

    @property
    def click_position_y_percentage_from_origin(self) -> int:
        """
        Get Y position as percentage from window origin that should be clicked before sending command.
        Return override if exists.
        If not, get position from command_group.window.

        :return: Y position as percentage to click.
        """
        if self.override_click_position_y_percentage_from_origin is not None:
            return self.override_click_position_y_percentage_from_origin
        return self.command_group.window.click_position_y_percentage_from_origin
