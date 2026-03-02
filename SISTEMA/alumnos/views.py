from django.shortcuts import render, redirect
from .models import Materia

def lista_materias(request):
    materias = Materia.objects.all()
    return render(request, 'alumnos/lista.html', {'materias': materias})


def agregar_materia(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        creditos = request.POST['creditos']
        horario = request.POST['horario']

        Materia.objects.create(
            nombre=nombre,
            creditos=creditos,
            horario=horario
        )
        return redirect('lista_materias')

    return render(request, 'alumnos/agregar.html')
def editar_materia(request, id):
    materia = Materia.objects.get(id=id)

    if request.method == "POST":
        materia.nombre = request.POST['nombre']
        materia.creditos = request.POST['creditos']
        materia.horario = request.POST['horario']
        materia.save()
        return redirect('lista_materias')

    return render(request, 'alumnos/editar.html', {'materia': materia})
def eliminar_materia(request, id):
    materia = Materia.objects.get(id=id)
    materia.delete()
    return redirect('lista_materias')