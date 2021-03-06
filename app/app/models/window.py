from django.db import models
from django.utils.text import slugify

from app.models.software import Software
from app.validators import CLICK_POSITION_PERCENTAGE_VALIDATOR


class Window(models.Model):
    title = models.TextField()
    slug_title = models.SlugField(blank=True, null=True)
    software = models.ForeignKey(
        Software, on_delete=models.RESTRICT, related_name="windows"
    )
    click_position_x_percentage_from_origin = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="X position as percentage from window origin that should be clicked",
        validators=(CLICK_POSITION_PERCENTAGE_VALIDATOR,),
    )
    click_position_y_percentage_from_origin = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Y position as percentage from window origin that should be clicked",
        validators=(CLICK_POSITION_PERCENTAGE_VALIDATOR,),
    )

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
