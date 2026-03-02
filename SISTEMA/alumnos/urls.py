from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_materias, name='lista_materias'),
    path('agregar/', views.agregar_materia, name='agregar_materia'),
    path('editar/<int:id>/', views.editar_materia, name='editar_materia'),
    path('eliminar/<int:id>/', views.eliminar_materia, name='eliminar_materia'),
]