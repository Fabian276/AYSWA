from django.urls import path
from . import views

app_name = "asistencias"

urlpatterns = [
    path("", views.home, name="home"),
    path("grupo/<int:grupo_id>/pasar-lista/", views.pasar_lista, name="pasar_lista"),
]