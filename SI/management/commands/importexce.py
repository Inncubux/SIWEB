from django.core.management.base import BaseCommand
import pandas as pd
from SI.models import EventoSismico

class Command(BaseCommand):
    help = 'Importa eventos sísmicos desde un Excel'

    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str, help='Ruta del archivo Excel')

    def handle(self, *args, **kwargs):
        archivo = kwargs['archivo']
        df = pd.read_excel(archivo)
        for _, row in df.iterrows():
            try:
                fecha = pd.to_datetime(row["Fecha"], errors="coerce").date() if pd.notnull(row["Fecha"]) else None

                hora = None
                if pd.notnull(row["Hora"]):
                    hora_dt = pd.to_datetime(row["Hora"], format="%H:%M:%S.%f", errors="coerce")
                    if not pd.isna(hora_dt):
                        hora = hora_dt.time()

                EventoSismico.objects.create(
                    fecha=fecha,
                    hora=hora,
                    latitud=row.get("Latitud"),
                    longitud=row.get("Longitud"),
                    profundidad=row.get("Profundidad (km)"),
                    magnitud_mw=row.get("Magnitud Mw"),
                    magnitud_mb=row.get("Magnitud mb"),
                    magnitud_ms=row.get("Magnitud Ms"),
                    scalar_moment=row.get("Scalar Moment"),
                    strike1=row.get("Strike1"),
                    dip1=row.get("Dip1"),
                    slip1=row.get("Slip1"),
                    strike2=row.get("Strike2"),
                    dip2=row.get("Dip2"),
                    slip2=row.get("Slip2"),
                    start=row.get("start")
                )
            except Exception as e:
                self.stderr.write(f"❌ Error en fila: {e}")
