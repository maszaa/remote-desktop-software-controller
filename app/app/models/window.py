from django.db import models
from django.utils.text import slugify

from app.models.software import Software


class Window(models.Model):
    title = models.TextField()
    slug_title = models.SlugField(blank=True, null=True)
    software = models.ForeignKey(
        Software, on_delete=models.RESTRICT, related_name="windows"
    )
    needs_clicking_center = models.BooleanField(default=False)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.software.name}: {self.title}"

    def save(self, *args, **kwargs):
        self.slug_title = slugify(self.title)
        super().save(*args, **kwargs)

    def get_url_path(self) -> str:
        """
        Returns url path to this Window.

        :return: str
        """
        return f"{self.software.slug_name}/{self.slug_title}/"
