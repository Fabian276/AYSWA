from django.db import models
from django.core.exceptions import ValidationError


class Alumno(models.Model):
    matricula = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.matricula} - {self.nombre}"


class Docente(models.Model):
    # podemos amarrarlo a auth.User despues
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre


class GrupoEscolar(models.Model):
    # podemos decir que 8A
    clave = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=120, blank=True)  # opcional

    def __str__(self):
        return self.clave


class InscripcionGrupo(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="grupos")
    grupo = models.ForeignKey(GrupoEscolar, on_delete=models.CASCADE, related_name="alumnos")
    activa = models.BooleanField(default=True)

    class Meta:
        unique_together = ("alumno", "grupo")

    def __str__(self):
        return f"{self.alumno} -> {self.grupo}"


class Materia(models.Model):
    clave = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.clave} - {self.nombre}"


class Asignacion(models.Model):
    """
    Une grupo escolar + materia + docente.
    Esto representa "la materia tal con el profe" para ese grupo.
    """
    grupo = models.ForeignKey(GrupoEscolar, on_delete=models.CASCADE, related_name="asignaciones")
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT, related_name="asignaciones")
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="asignaciones")
    activa = models.BooleanField(default=True)

    class Meta:
        unique_together = ("grupo", "materia", "docente")

    def __str__(self):
        return f"{self.grupo} | {self.materia} | {self.docente}"


class SesionClase(models.Model):
    """
    Una sesion real de clase: en una fecha, en un bloque del día (1..6)
    y para una asignacion (grupo+muestra+mestro).
    """
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE, related_name="sesiones")
    fecha = models.DateField()
    bloque = models.PositiveSmallIntegerField()  # 1..6

    class Meta:
        unique_together = ("asignacion", "fecha", "bloque")
        ordering = ["-fecha", "bloque"]

    def clean(self):
        if not (1 <= self.bloque <= 6):
            raise ValidationError("bloque debe estar entre 1 y 6.")

    def __str__(self):
        return f"{self.asignacion} | {self.fecha} | Bloque {self.bloque}"


class Asistencia(models.Model):
    ESTADOS = [
        ("P", "Presente"),
        ("A", "Ausente"),
        ("R", "Retardo"),
        ("J", "Justificado"),
    ]

    sesion = models.ForeignKey(SesionClase, on_delete=models.CASCADE, related_name="asistencias")
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="asistencias")
    estado = models.CharField(max_length=1, choices=ESTADOS, default="A")
    comentario = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("sesion", "alumno")

    def __str__(self):
        return f"{self.sesion} | {self.alumno} -> {self.get_estado_display()}"