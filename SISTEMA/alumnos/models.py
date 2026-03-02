from django.db import models

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    creditos = models.IntegerField()
    horario = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre