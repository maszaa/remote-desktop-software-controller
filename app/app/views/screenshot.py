from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from app.models import Window
from app.screenshot import Screenshot


class ScreenshotView(View):
    model = Window

    def get(self, request):
        software, window = [
            text
            for text in self.request.path.split("/")
            if text and text != "screenshot"
        ]
        window = self.model.objects.filter(
            title=window, software__name=software
        ).first()
        image_data = Screenshot(window.title).capture()
        return HttpResponse(
            image_data, content_type=f"image/{settings.SCREENSHOT_IMAGE_FORMAT}"
        )
