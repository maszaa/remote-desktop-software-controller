import traceback

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse
from django.views.generic import DetailView

from app.models import Command, Window
from app.window_control import WindowControl


class WindowView(LoginRequiredMixin, DetailView):
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

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            self.object = self.get_object()
            command = self._get_command()
            sent = WindowControl(command.command_group.window.title).send_key(
                command.command,
                command.command_group.window.click_position_x_percentage_from_origin,
                command.command_group.window.click_position_y_percentage_from_origin,
            )
        except Exception as e:
            settings.LOGGER.error(traceback.format_exc())
            return JsonResponse(str(e), status=500, safe=False)

        if sent is True:
            return JsonResponse("OK", status=200, safe=False)
        elif sent is False:
            return JsonResponse(
                f"Window {self.object.title} not found", status=404, safe=False
            )
        else:
            return JsonResponse("Unknown error", status=500, safe=False)

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
