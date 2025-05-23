from django.db import models

class EventoSismico(models.Model):
    fecha = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    profundidad = models.FloatField(null=True, blank=True)
    magnitud_mw = models.FloatField(null=True, blank=True)
    magnitud_mb = models.FloatField(null=True, blank=True)
    magnitud_ms = models.FloatField(null=True, blank=True)
    scalar_moment = models.CharField(max_length=50, null=True, blank=True)
    strike1 = models.FloatField(null=True, blank=True)
    dip1 = models.FloatField(null=True, blank=True)
    slip1 = models.FloatField(null=True, blank=True)
    strike2 = models.FloatField(null=True, blank=True)
    dip2 = models.FloatField(null=True, blank=True)
    slip2 = models.FloatField(null=True, blank=True)
    start = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fecha} {self.hora} - Mw {self.magnitud_mw}"
