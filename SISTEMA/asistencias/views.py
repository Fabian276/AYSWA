from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    GrupoEscolar, Asignacion, InscripcionGrupo,
    SesionClase, Asistencia
)

ESTADOS = [
    ("P", "Presente"),
    ("A", "Ausente"),
    ("R", "Retardo"),
    ("J", "Justificado"),
]

def home(request):
    # Lista de grupos para iniciar
    grupos = GrupoEscolar.objects.all().order_by("clave")
    return render(request, "asistencias/home.html", {"grupos": grupos})


def pasar_lista(request, grupo_id):
    grupo = get_object_or_404(GrupoEscolar, id=grupo_id)

    # Asignaciones activas del grupo (materia+docente)
    asignaciones = Asignacion.objects.filter(grupo=grupo, activa=True).select_related("materia", "docente").order_by("materia__nombre")

    # --- Crear/Abrir sesión ---
    if request.method == "POST" and request.POST.get("accion") == "abrir_sesion":
        asignacion_id = int(request.POST["asignacion_id"])
        fecha_str = request.POST["fecha"]
        bloque = int(request.POST["bloque"])

        asignacion = get_object_or_404(Asignacion, id=asignacion_id, grupo=grupo)

        # Crear sesión única por asignación+fecha+bloque
        sesion, _ = SesionClase.objects.get_or_create(
            asignacion=asignacion,
            fecha=fecha_str,
            bloque=bloque,
        )

        # Crear asistencia default (Ausente) para todos los alumnos inscritos activos al grupo
        inscripciones = InscripcionGrupo.objects.filter(grupo=grupo, activa=True).select_related("alumno")
        for ins in inscripciones:
            Asistencia.objects.get_or_create(
                sesion=sesion,
                alumno=ins.alumno,
                defaults={"estado": "A"},
            )

        return redirect(f"/grupo/{grupo.id}/pasar-lista/?sesion={sesion.id}")

    # --- Si ya hay sesión seleccionada, mostrar lista ---
    sesion = None
    asistencias = []
    sesion_id = request.GET.get("sesion")

    # Para selector: últimas sesiones del grupo (las últimas 25)
    ultimas_sesiones = SesionClase.objects.filter(asignacion__grupo=grupo).select_related(
        "asignacion__materia", "asignacion__docente"
    ).order_by("-fecha", "-bloque")[:25]

    if sesion_id:
        sesion = get_object_or_404(SesionClase, id=sesion_id, asignacion__grupo=grupo)
        asistencias = Asistencia.objects.filter(sesion=sesion).select_related("alumno").order_by("alumno__nombre")

        # Guardar cambios
        if request.method == "POST" and request.POST.get("accion") == "guardar":
            for a in asistencias:
                nuevo = request.POST.get(f"estado_{a.id}")
                comentario = request.POST.get(f"comentario_{a.id}", "")
                if nuevo in {"P", "A", "R", "J"}:
                    a.estado = nuevo
                    a.comentario = comentario.strip()
                    a.save()
            return redirect(f"/grupo/{grupo.id}/pasar-lista/?sesion={sesion.id}")

    return render(
        request,
        "asistencias/pasar_lista.html",
        {
            "grupo": grupo,
            "asignaciones": asignaciones,
            "ultimas_sesiones": ultimas_sesiones,
            "sesion": sesion,
            "asistencias": asistencias,
            "hoy": date.today().isoformat(),
            "estados": ESTADOS,
        },
    )