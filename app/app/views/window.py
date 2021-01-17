import traceback
from typing import Optional

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
    window_control = None

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
            self.window_control = WindowControl(self.object.title)
            sent = self._handle_request()
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

    def _get_command(self, command: str) -> Command:
        """
        Get command to be executed.

        :param command: Command as str to search for
        :return: Command
        """
        return (
            Command.objects.filter(
                name=command,
                command_group__window__title=self.object.title,
                command_group__window__software__name=self.object.software.name,
            )
            .select_related("command_group__window", "key")
            .first()
        )

    def _handle_request(self) -> Optional[bool]:
        """
        Handle user's command request.

        :return: True, if command was executed, False otherwise
        :raises KeyError: if command or clickX and clickY aren't present in request payload
        """
        command = self.request.POST.get("command")

        if command:
            command = self._get_command(command)
            return self.window_control.send_key(
                command.command,
                command.click_position_x_percentage_from_origin,
                command.click_position_y_percentage_from_origin,
            )
        else:
            click_x, click_y = (
                self.request.POST.get("clickX"),
                self.request.POST.get("clickY"),
            )

            if click_x and click_y:
                return self.window_control.send_click(float(click_x), float(click_y))
            else:
                from_x, from_y, to_x, to_y = (
                    self.request.POST.get("fromX"),
                    self.request.POST.get("fromY"),
                    self.request.POST.get("toX"),
                    self.request.POST.get("toY"),
                )

                if from_x and from_y and to_x and to_y:
                    return self.window_control.send_drag(
                        float(from_x),
                        float(from_y),
                        float(to_x),
                        float(to_y),
                    )

        raise KeyError(
            "Either command or clickX and clickY or fromX, fromY, toX and toY must be present in request payload"
        )
