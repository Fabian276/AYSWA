from django.contrib import admin
from .models import (
    Alumno, Docente, GrupoEscolar, InscripcionGrupo,
    Materia, Asignacion, SesionClase, Asistencia
)

admin.site.register(Alumno)
admin.site.register(Docente)
admin.site.register(GrupoEscolar)
admin.site.register(InscripcionGrupo)
admin.site.register(Materia)
admin.site.register(Asignacion)
admin.site.register(SesionClase)
admin.site.register(Asistencia)