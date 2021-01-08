from django.db import models

from app.models.window import Window


class CommandGroup(models.Model):
    name = models.TextField(blank=False)
    order = models.PositiveIntegerField(default=0)
    window = models.ForeignKey(
        Window, on_delete=models.CASCADE, related_name="command_groups"
    )

    class Meta:
        ordering = ["order", "name"]

    def __str__(self) -> str:
        command_group = (
            self.__class__.objects.filter(pk=self.pk)
            .select_related("window__software")
            .first()
        )
        software = command_group.window.software.name
        window = command_group.window.title

        return f"{software}: {window} - {self.order}. {self.name}"
