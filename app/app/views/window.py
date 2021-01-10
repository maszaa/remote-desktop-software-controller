from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView

from app.models import Command, Window
from app.window_control import WindowControl


class WindowView(DetailView):
    model = Window
    template_name = "window.pug"

    def get_queryset(self) -> QuerySet:
        return (
            self.model.objects.filter(
                slug_title=self.kwargs.get("window"),
                software__slug_name=self.kwargs.get("software"),
            )
            .select_related("software")
            .prefetch_related("command_groups__commands")
        )

    def get_object(self, queryset: QuerySet = None) -> Window:
        return self.get_queryset().first()

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        command = self._get_command()
        WindowControl(command.command_group.window.title).send_key(
            command.command, command.command_group.window.needs_clicking_center
        )
        return redirect(f"/{self.object.get_url_path()}", permanent=True)

    def _get_command(self) -> Command:
        """
        Get command to be executed.

        :return: Command
        """
        return (
            Command.objects.filter(
                name=self.request.POST["command"],
                command_group__window__title=self.object.title,
                command_group__window__software__name=self.object.software.name,
            )
            .select_related("command_group__window", "key")
            .first()
        )
