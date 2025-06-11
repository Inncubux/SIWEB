from django.shortcuts import render
from .models import EventoSismico  # Ajusta el nombre del modelo si es necesario
from django.core.paginator import Paginator

def resultados_terremotos(request):
    terremotos = EventoSismico.objects.all()

    # Filtros por fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_final = request.GET.get('fecha_final')
    if fecha_inicio:
        terremotos = terremotos.filter(fecha__gte=fecha_inicio)
    if fecha_final:
        terremotos = terremotos.filter(fecha__lte=fecha_final)

    # Filtros por latitud y longitud
    latitud_min = request.GET.get('latitud_min')
    latitud_max = request.GET.get('latitud_max')
    longitud_min = request.GET.get('longitud_min')
    longitud_max = request.GET.get('longitud_max')
    if latitud_min:
        terremotos = terremotos.filter(latitud__gte=latitud_min)
    if latitud_max:
        terremotos = terremotos.filter(latitud__lte=latitud_max)
    if longitud_min:
        terremotos = terremotos.filter(longitud__gte=longitud_min)
    if longitud_max:
        terremotos = terremotos.filter(longitud__lte=longitud_max)

    # Filtros por magnitud
    magnitud_min = request.GET.get('magnitud')
    magnitud_max = request.GET.get('magnitud_max')
    if magnitud_min:
        terremotos = terremotos.filter(magnitud_mw__gte=magnitud_min)
    if magnitud_max:
        terremotos = terremotos.filter(magnitud_mw__lte=magnitud_max)

    # Paginación (10 resultados por página)
    paginator = Paginator(terremotos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'resultados.html', {
        'resultados': page_obj,
        'request': request  # Para mostrar los filtros aplicados en la plantilla
    })

def buscar_terremotos(request):
    return render(request, 'base.html')
