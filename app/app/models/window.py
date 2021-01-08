from django.db import models

from app.models.software import Software


class Window(models.Model):
    title = models.TextField()
    software = models.ForeignKey(
        Software, on_delete=models.RESTRICT, related_name="windows"
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.software.name}: {self.title}"
