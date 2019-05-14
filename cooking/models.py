from django.db import models

# Create your models here.

class Lote(models.Model):
    """
    Modelo que representa un lote
    """
    lote_nro = models.PositiveIntegerField(help_text="ID lote, debe ser unico",
            primary_key=True, null=False)
    observaciones = models.TextField(max_length=100,
            help_text="Comentarios,datos o informacion relevante a un lote determinado", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # listamos los lotes con el mas reciente primero
    class Meta:
        ordering = ["-fecha_creacion"]


    def __str__(self):
        return str(self.lote_nro)


class SeguimientoMaceracionCoccion(models.Model):
    """
    Primer proceso de la elaboración, se distingue todo el proceso por un ID unico, el lote_nro
    """
    lote = models.OneToOneField(Lote, on_delete=models.CASCADE, primary_key=True)
    fecha_inicio = models.DateField(help_text="Fecha inicio del proceso de coccion, campo requerido",null=True,blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    observaciones = models.TextField(max_length=100, help_text="Comentarios,datos o informacion relevante para un lote determinado", null=True, blank=True)

    def __str__(self):
        return str(f"Planilla de Maceración/Cocción - Lote número {self.lote.lote_nro}")

class Maceracion(models.Model):
    """
    Etapa general de maceracion, puede ser batch_nro 1 o 2
    """
    NRO_BATCH = (
        (1, 1),
        (2, 2),
    )
    batch_nro = models.PositiveIntegerField(choices=NRO_BATCH, help_text="nro de batch correspondiente, puede ser 1 o 2")
    seguimiento_maceracion_coccion = models.ForeignKey('SeguimientoMaceracionCoccion', on_delete=models.CASCADE, null=True)
    densidad_finalizacion_maceracion = models.FloatField(null=True, blank=True)
    densidad_finalizacion_lavado = models.FloatField(null=True, blank=True)
    observaciones = models.TextField(max_length=100, help_text="Comentarios,datos o informacion relevante a la etapa de maceracion", null=True, blank=True)

    def __str__(self):
        return str(f"Maceracion - Lote {self.seguimiento_maceracion_coccion.lote.lote_nro} - Batch número {self.batch_nro}")

class Correccion(models.Model):
    """
    Registro de correccion del PH para una etapa de maceracion/batch determinada
    """
    maceracion = models.ForeignKey('Maceracion', on_delete=models.CASCADE, null=True)
    inicial = models.FloatField(blank=True, null=True)
    acido_fosforico = models.FloatField(null=True, blank=True)
    final_maceracion = models.FloatField(null=True, blank=True)


class OllaMaceracion(models.Model):
    """
    Clase Registro de datos tomdos de la Olla de Maceracion, tipo de granos, cantidad en kilogramos y agua (L)
    """
    maceracion = models.ForeignKey('Maceracion', on_delete=models.CASCADE, null=True)
    granos = models.CharField(max_length=50, help_text="Tipo de grano",blank=True)
    cantidad = models.FloatField(null=True, blank=True, help_text='Cantidad expresada en kilogramos')
    agua = models.CharField(max_length=50, help_text="Litros", null=True, blank=True)


class OllaAguaCaliente(models.Model):
    """
    Clase que representa el proceso durante Olla de agua Caliente
    """
    maceracion = models.ForeignKey('Maceracion', on_delete=models.CASCADE, null=True)
    agua_dureza = models.CharField(max_length=50, help_text="dureza de agua dentro de Olla caliente", null=True, blank=True)
    agua_ph = models.CharField(max_length=50, help_text="ph del agua dentro Olla caliente", null=True, blank=True)
    filtracion_hora_inicio = models.CharField(max_length=50, help_text="hora inicio de filtracion")


class EtapaOllaAguaCaliente(models.Model):
    """
    Etapa perteneciente a la Olla de agua caliente, por ahora solo existen "empaste" y "maceracion"
    """
    olla_agua_caliente = models.ForeignKey('OllaAguaCaliente', on_delete=models.CASCADE, null=True)
    NOMBRE_ETAPA = (
        ('empaste', 'Empaste'),
        ('maceracion', 'Maceracion'),
    )
    etapa_nombre = models.CharField(max_length=50, choices=NOMBRE_ETAPA, help_text="etapa nombre, solo puede ser Empaste o Maceracion")
    etapa_hora_inicio = models.CharField(max_length=50, help_text="hora inicio")
    temperatura_R = models.CharField(max_length=50, null=True, blank=True)
    temperatura_M = models.CharField(max_length=50, null=True, blank=True)
    altura = models.CharField(max_length=50, null=True, blank=True)
    agit_rec = models.CharField(max_length=50, help_text="", null=True, blank=True)


## Proceso de Cocccion

class Coccion(models.Model):
    """
    Etapa general de maceracion, puede ser batch_nro 1 o 2
    """
    proceso_maceracion_coccion = models.ForeignKey('SeguimientoMaceracionCoccion', on_delete=models.CASCADE, null=True)
    NRO_BATCH = (
        (1, 1),
        (2, 2),
    )
    batch_nro = models.PositiveIntegerField(choices=NRO_BATCH, help_text="nro de batch correspondiente, puede ser 1 o 2")
    densidad_finalizacion_hervor = models.FloatField(null=True, blank=True)
    hora_fin_trasiego = models.CharField(max_length=50, help_text="hora inicio", null=True, blank=True)
    observaciones = models.TextField(max_length=100, help_text="Comentarios,datos o informacion relevante a la etapa de coccion", null=True, blank=True)


class EtapaCoccion(models.Model):
    """
    Clase que describe una etapa de coccion, actualmente pueden ser 5, Lavado, Aumento T, Hervor, Reposos y Trasiego
    """
    coccion = models.ForeignKey('Coccion', on_delete=models.CASCADE, null=True)
    etapa_hora_inicio = models.CharField(max_length=50, help_text="hora inicio")
    NOMBRE_ETAPA = (
        ('lavado', 'lavado'),
        ('aumento T', 'aumento T'),
        ('hervor', 'hervor'),
        ('reposo', 'reposo'),
        ('trasiego', 'trasiego'),
    )
    etapa_nombre = models.CharField(max_length=50, choices=NOMBRE_ETAPA, help_text="etapa nombre, solo puede ser Lavado, Aumento T, Hervor, Reposos y Trasiego")


class Adicion(models.Model):
    """
    Clase que representa una adicion a una etapa de coccion determinada
    """
    etapa_coccion = models.ForeignKey('EtapaCoccion', on_delete=models.CASCADE, null=True, help_text="Etapa de Coccion a la que pertenece dicha adicion")
    tipo = models.CharField(max_length=50, help_text="Tipo de adicion")
    gramos = models.PositiveIntegerField(null=True, blank=True, help_text='Cantidad expresada en gramos')
    hora_adicion = models.CharField(max_length=50, help_text="hora de adicion", null=True, blank=True)


class SeguimientoFermentacionClarificacion(models.Model):
    """
    Segundo proceso de la elaboración, se distingue todo el proceso por un ID unico, el lote_nro
    """
    lote = models.OneToOneField(Lote, on_delete=models.CASCADE, primary_key=True)
    fecha_inicio = models.DateField(help_text="Fecha inicio del proceso de fermentacion, campo requerido")
    fecha_fin = models.DateField(null=True, blank=True)
    observaciones = models.TextField(max_length=200, help_text="Comentarios,datos o información relevante al seguimiento de fermentacion para un lote determinado", null=True, blank=True)

    def __str__(self):
        return str(f"Planilla de Fermentación/Clarificación - Lote número {self.lote.lote_nro}")


class SeguimientoCarbonatacion(models.Model):
    """
    Tercer seguimiento de la elaboración, se distingue todo el suiemiento por un ID único, el lote_nro
    """
    fecha_inicio = models.DateField(help_text="Fecha inicio del proceso de carbonatación, campo requerido")
    fecha_fin = models.DateField(null=True, blank=True)
    lote = models.OneToOneField(Lote, on_delete=models.CASCADE, primary_key=True)
    observaciones = models.TextField(max_length=200, help_text="Comentarios,datos o informacion relevante al seguimiento de carbonatación para un lote determinado", null=True, blank=True)

    def __str__(self):
        return str(f"Planilla de Carbonatación - Lote número {self.lote.lote_nro}")
