from django.db import models
from django.utils.text import slugify


class Software(models.Model):
    name = models.TextField()
    slug_name = models.SlugField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super().save(*args, **kwargs)
