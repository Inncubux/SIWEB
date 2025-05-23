import pandas as pd
from django.core.management.base import BaseCommand
from SI.models import EventoSismico
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa datos desde un archivo Excel a la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str, help='Ruta del archivo Excel')

    def handle(self, *args, **kwargs):
        archivo = kwargs['archivo']
        df = pd.read_excel(archivo)

        eventos_creados = 0
        for _, row in df.iterrows():
            try:
                evento = EventoSismico(
                    fecha=pd.to_datetime(row['Fecha'], errors='coerce').date() if pd.notnull(row['Fecha']) else None,
                    hora=pd.to_datetime(str(row['Hora']), errors='coerce').time() if pd.notnull(row['Hora']) else None,
                    latitud=row.get('Latitud'),
                    longitud=row.get('Longitud'),
                    profundidad=row.get('Profundidad (km)'),
                    magnitud_mw=row.get('Magnitud Mw'),
                    magnitud_mb=row.get('Magnitud mb'),
                    magnitud_ms=row.get('Magnitud Ms'),
                    scalar_moment=row.get('Scalar Moment'),
                    strike1=row.get('Strike1'),
                    dip1=row.get('Dip1'),
                    slip1=row.get('Slip1'),
                    strike2=row.get('Strike2'),
                    dip2=row.get('Dip2'),
                    slip2=row.get('Slip2'),
                    start=row.get('start')
                )
                evento.save()
                eventos_creados += 1
            except Exception as e:
                self.stderr.write(f"⚠️ Error en fila: {e}")

        self.stdout.write(self.style.SUCCESS(f"✅ {eventos_creados} eventos importados con éxito"))
