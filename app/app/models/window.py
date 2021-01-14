from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.text import slugify

from app.models.software import Software

CLICK_POSITION_PERCENTAGE_VALIDATOR = MaxValueValidator(
    100, message="Click position percentage must be in range of 0 to 100"
)


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
