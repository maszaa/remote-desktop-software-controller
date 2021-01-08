from django.db import models

from app.models.command_group import CommandGroup
from app.models.key import Key


class Command(models.Model):
    name = models.TextField(blank=False)
    order = models.PositiveIntegerField(default=0)
    command_group = models.ForeignKey(
        CommandGroup, on_delete=models.CASCADE, related_name="commands"
    )
    key = models.ForeignKey(Key, null=True, on_delete=models.RESTRICT)
    multiplier = models.PositiveIntegerField(default=1)
    free_text = models.TextField()

    class Meta:
        ordering = ["order", "name"]

    def __str__(self) -> str:
        command = (
            self.__class__.objects.filter(pk=self.pk)
            .select_related("command_group__window__software")
            .first()
        )
        software = command.command_group.window.software.name
        window = command.command_group.window.title
        command_group = command.command_group.name

        return f"{software}: {window} - {command_group}: {self.order}. {self.command}"

    @property
    def command(self) -> str:
        if self.key:
            return "".join(self.key.key for i in range(self.multiplier))
        return self.free_text
