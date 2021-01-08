"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys

from django.contrib import admin
from django.urls import path

from app.models import Software
from app.views import SoftwareListView, WindowView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", SoftwareListView.as_view(), name="Software window list"),
]

if not set(sys.argv).intersection(set(["makemigrations", "migrate"])):
    for software in Software.objects.all().prefetch_related("windows"):
        for window in software.windows.all():
            urlpatterns.append(
                path(
                    f"{software.name}/{window.title}/",
                    WindowView.as_view(),
                    name=f"Software window {software.name} - {window.title}",
                )
            )
