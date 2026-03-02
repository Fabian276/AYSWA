from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("asistencias.urls")),
]
    path('', include('alumnos.urls')),
]
