from django.http import HttpResponse
from django.views.generic import View

from app.models import Window


class WindowView(View):
    def get(self, request):
        software, window = [text for text in request.path.split("/") if text]
        window = Window.objects.get(title=window, software__name=software)
        return HttpResponse(str(vars(window)))
