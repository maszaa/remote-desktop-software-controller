from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
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
            slug_title=window, software__slug_name=software
        ).first()
        image_data = Screenshot(window.title).capture()

        if not image_data:
            raise Http404("Window not open or screenshot not captured for some reason")

        return HttpResponse(
            image_data, content_type=f"image/{settings.SCREENSHOT_IMAGE_FORMAT}"
        )
