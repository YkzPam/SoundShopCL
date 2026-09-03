"""Rutas principales del proyecto SoundShop CL."""

from django.urls import include, path


urlpatterns = [
    path("", include("core.urls")),
]
