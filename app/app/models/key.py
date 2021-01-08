from django.db import models


class Key(models.Model):
    key = models.TextField(blank=False, unique=True)

    class Meta:
        ordering = ["key"]

    def __str__(self) -> str:
        return self.key
