from django.db.models import QuerySet
from django.views.generic import ListView

from app.models import Software


class SoftwareListView(ListView):
    model = Software
    template_name = "softwares.pug"

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all()
