from django.shortcuts import render, redirect
from .models import EventoSismico

def buscar_terremotos(request):
    return render(request, 'base.html')

def resultados_terremotos(request):
    resultados = EventoSismico.objects.all()

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_final = request.GET.get('fecha_final')
    latitud = request.GET.get('latitud')
    longitud = request.GET.get('longitud')
    magnitud = request.GET.get('magnitud')

    if fecha_inicio:
        resultados = resultados.filter(fecha__gte=fecha_inicio)
    if fecha_final:
        resultados = resultados.filter(fecha__lte=fecha_final)
    if latitud:
        resultados = resultados.filter(latitud=latitud)
    if longitud:
        resultados = resultados.filter(longitud=longitud)
    if magnitud:
        resultados = resultados.filter(magnitud_mw__gte=magnitud)

    return render(request, 'resultados.html', {'resultados': resultados})
