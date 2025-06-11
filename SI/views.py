from django.shortcuts import render
from .models import EventoSismico  # Ajusta el nombre del modelo si es necesario
from django.core.paginator import Paginator
import openpyxl
from django.http import HttpResponse

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

def descargar_excel(request):
    terremotos = EventoSismico.objects.all()

    # Aplica los mismos filtros que en resultados_terremotos
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_final = request.GET.get('fecha_final')
    latitud_min = request.GET.get('latitud_min')
    latitud_max = request.GET.get('latitud_max')
    longitud_min = request.GET.get('longitud_min')
    longitud_max = request.GET.get('longitud_max')
    magnitud_min = request.GET.get('magnitud')
    magnitud_max = request.GET.get('magnitud_max')

    if fecha_inicio:
        terremotos = terremotos.filter(fecha__gte=fecha_inicio)
    if fecha_final:
        terremotos = terremotos.filter(fecha__lte=fecha_final)
    if latitud_min:
        terremotos = terremotos.filter(latitud__gte=latitud_min)
    if latitud_max:
        terremotos = terremotos.filter(latitud__lte=latitud_max)
    if longitud_min:
        terremotos = terremotos.filter(longitud__gte=longitud_min)
    if longitud_max:
        terremotos = terremotos.filter(longitud__lte=longitud_max)
    if magnitud_min:
        terremotos = terremotos.filter(magnitud_mw__gte=magnitud_min)
    if magnitud_max:
        terremotos = terremotos.filter(magnitud_mw__lte=magnitud_max)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append([
        'Fecha', 'Hora', 'Latitud', 'Longitud', 'Profundidad', 'Magnitud Mw', 'Magnitud mb', 'Magnitud Ms',
        'Scalar Moment', 'Strike1', 'Dip1', 'Slip1', 'Strike2', 'Dip2', 'Slip2'
    ])
    for t in terremotos:
        ws.append([
            t.fecha, t.hora, t.latitud, t.longitud, t.profundidad, t.magnitud_mw, t.magnitud_mb, t.magnitud_ms,
            t.scalar_moment, t.strike1, t.dip1, t.slip1, t.strike2, t.dip2, t.slip2
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=terremotos.xlsx'
    wb.save(response)
    return response
