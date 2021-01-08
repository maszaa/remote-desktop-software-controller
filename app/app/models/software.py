from django.db import models


class Software(models.Model):
    name = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
