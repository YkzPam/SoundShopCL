from django.urls import include, path

# El caso utiliza su propio panel, no el administrador de base de datos.
urlpatterns = [path("", include("core.urls"))]
