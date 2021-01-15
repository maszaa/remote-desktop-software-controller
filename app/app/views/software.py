from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView

from app.models import Software, Window


class SoftwareListView(LoginRequiredMixin, ListView):
    model = Software
    template_name = "softwares.pug"

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all().prefetch_related("windows")

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Render a list of software and windows of those.
        If only one software window is configured, redirect user to the control view of that window.

        :return: List of softwares with their windows or a redirect as HttpResponse
        """
        response = super().get(request, *args, **kwargs)
        window = self._determine_redirect_to_only_software_window()

        if window:
            return redirect(window.get_url_path())
        return response

    def _determine_redirect_to_only_software_window(self) -> Optional[Window]:
        """
        If only one software window exists in configuration return that.
        Otherwise return None.

        :return: Window or None
        """
        windows = [
            window for software in self.object_list for window in software.windows.all()
        ]

        return None if len(windows) != 1 else windows.pop()
