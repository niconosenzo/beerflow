
from django.db import models
from .utils import constants
from .utils.models import CreationModificationDateMixin
from datetime import time


# Create your models here.


class Lote(CreationModificationDateMixin):
    """
    Modelo que representa un lote
    """
    lote_nro = models.PositiveIntegerField(help_text="ID lote, debe ser unico",
                                           primary_key=True, null=False)
    observaciones = models.TextField(max_length=100,
                                     null=True, blank=True)
    # fecha_creacion = models.DateTimeField(auto_now_add=True)
    # listamos los lotes con el mas reciente primero

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return str(self.lote_nro)


class Barril(CreationModificationDateMixin):
    """
    Modelo que representa un lote
    """
    barril_nro = models.CharField(max_length=20,
                                  help_text="ID barril, debe ser unico",
                                  primary_key=True, null=False)
    observaciones = models.TextField(max_length=100,
                                     null=True, blank=True)

    # listamos los lotes con el mas reciente primero

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return str(self.barril_nro)


class MovimientosBarril(CreationModificationDateMixin):
    """
    Modelo para registrar movientos de un barrir para un lote determinado
    """
    # fecha = models.DateField()
    barril = models.ForeignKey(
        'Barril', on_delete=models.CASCADE, null=True)
    lote = models.ForeignKey(
        'Lote', on_delete=models.CASCADE, null=True)
    cliente = models.CharField(max_length=20,
                               help_text="Cliente, obligatorio")
    ingresa = models.DateField(null=True, blank=True)
    egresa = models.DateField(null=True, blank=True)
    estado_devolucion = models.CharField(max_length=20,
                                         choices=constants.DEVOLUCION,
                                         null=True, blank=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        mov = "Movimiento de barril " + \
            str(self.barril) + " - lote " + str(self.lote)
        return mov


# PLANILLA MACERACION COCCION

class SeguimientoMaceracionCoccion(CreationModificationDateMixin):
    """
    Primer proceso de la elaboración,
    se distingue todo el proceso por un ID unico, el lote_nro
    """
    lote = models.OneToOneField(
        Lote, on_delete=models.CASCADE, primary_key=True)
    #fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    observaciones = models.TextField(
        max_length=100,  null=True, blank=True)

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
    batch_nro = models.PositiveIntegerField(choices=NRO_BATCH)
    seguimiento_maceracion_coccion = models.ForeignKey(
        'SeguimientoMaceracionCoccion', on_delete=models.CASCADE, null=True)
    densidad_finalizacion_maceracion = models.FloatField(null=True, blank=True)
    densidad_finalizacion_lavado = models.FloatField(null=True, blank=True)
    observaciones = models.TextField(
        max_length=100, null=True, blank=True)

    def __str__(self):
        return str(f"Maceracion - Lote {self.seguimiento_maceracion_coccion.lote.lote_nro} - Batch número {self.batch_nro}")


class Correccion(models.Model):
    """
    Registro de correccion del PH para una
    etapa de maceracion/batch determinada
    """
    maceracion = models.ForeignKey(
        'Maceracion', on_delete=models.CASCADE, null=True)
    inicial = models.FloatField(blank=True, null=True)
    acido_fosforico = models.FloatField(null=True, blank=True)
    final_maceracion = models.FloatField(null=True, blank=True)


class OllaMaceracion(models.Model):
    """
    Clase Registro de datos tomdos de la Olla de Maceracion,
    tipo de granos, cantidad en kilogramos y agua (L)
    """
    maceracion = models.ForeignKey(
        'Maceracion', on_delete=models.CASCADE, null=True)
    granos = models.CharField(
        max_length=20, help_text="Tipo de grano", blank=True)
    cantidad = models.FloatField(
        null=True, blank=True, help_text='Cantidad expresada en kilogramos')
    agua = models.CharField(
        max_length=20, help_text="Litros", null=True, blank=True)


class OllaAguaCaliente(models.Model):
    """
    Clase que representa el proceso durante Olla de agua Caliente
    """

    maceracion = models.ForeignKey(
        'Maceracion', on_delete=models.CASCADE, null=True)
    agua_dureza = models.CharField(
        max_length=20, help_text="dureza de agua dentro de Olla caliente",
        null=True, blank=True)
    agua_ph = models.CharField(
        max_length=20, help_text="ph del agua dentro Olla caliente",
        null=True, blank=True)
    filtracion_hora_inicio = models.TimeField(
        choices=constants.HORA, null=True, blank=True)
    filtracion_temperatura = models.CharField(
        max_length=20, null=True, blank=True)


class EtapaOllaAguaCaliente(models.Model):
    """
    Etapa perteneciente a la Olla de agua caliente,
    por ahora solo existen "empaste" y "maceracion"
    """
    olla_agua_caliente = models.ForeignKey(
        'OllaAguaCaliente', on_delete=models.CASCADE, null=True)
    NOMBRE_ETAPA = (
        ('empaste', 'Empaste'),
        ('maceracion', 'Maceracion'),
    )
    etapa_nombre = models.CharField(max_length=20, choices=NOMBRE_ETAPA,
                                    help_text="etapa nombre, solo puede ser Empaste o Maceracion")
    etapa_hora_inicio = models.TimeField(
        choices=constants.HORA, null=True, blank=True)
    temperatura_R = models.CharField(max_length=10, null=True, blank=True)
    temperatura_M = models.CharField(max_length=10, null=True, blank=True)
    altura = models.CharField(max_length=10, null=True, blank=True)
    agit_rec = models.CharField(
        max_length=10, help_text="", null=True, blank=True)


# Proceso de Cocccion

class Coccion(models.Model):
    """
    Etapa general de maceracion, puede ser batch_nro 1 o 2
    """
    proceso_maceracion_coccion = models.ForeignKey(
        'SeguimientoMaceracionCoccion', on_delete=models.CASCADE, null=True)
    NRO_BATCH = (
        (1, 1),
        (2, 2),
    )
    batch_nro = models.PositiveIntegerField(
        choices=NRO_BATCH, help_text="nro de batch correspondiente, puede ser 1 o 2")
    densidad_finalizacion_hervor = models.FloatField(null=True, blank=True)
    hora_fin_trasiego = models.TimeField(
        choices=constants.HORA, null=True, blank=True)
    observaciones = models.TextField(
        max_length=50, null=True, blank=True)


class EtapaCoccion(models.Model):
    """
    Clase que describe una etapa de coccion,
    actualmente pueden ser 5, Lavado, Aumento T, Hervor, Reposos y Trasiego
    """
    coccion = models.ForeignKey('Coccion', on_delete=models.CASCADE, null=True)
    NOMBRE_ETAPA = (
        ('Lavado', 'Lavado'),
        ('Aumento T', 'Aumento T'),
        ('Hervor', 'Hervor'),
        ('Reposo', 'Reposo'),
        ('Trasiego', 'Trasiego'),
    )
    etapa_nombre = models.CharField(max_length=20)
    etapa_hora_inicio = models.TimeField(
        choices=constants.HORA, null=True, blank=True)
    # según planilla, cada etpa solo tiene una adicion


class AdicionCoccion(models.Model):
    """
    Clase que representa una adicion durante la etapa de hervor para una
    coccion determinada
    """
    # etapa_coccion = models.ForeignKey(
    #     'EtapaCoccion', on_delete=models.CASCADE, null=True)
    coccion = models.ForeignKey('Coccion', on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=20, help_text="Tipo de adicion")
    gramos = models.PositiveIntegerField(
        null=True, blank=True, help_text='Cantidad expresada en gramos')
    hora_adicion = models.TimeField(
        choices=constants.HORA, null=True, blank=True)


# PLANILLA CONTROL DE FERMENTACION


class ParametrosFundamentales(models.Model):
    lote = models.OneToOneField(
        Lote, on_delete=models.CASCADE, primary_key=True)
    dO = models.CharField(max_length=10, null=True, blank=True)
    dF = models.CharField(max_length=10, null=True, blank=True)
    alcohol_teorico = models.CharField(max_length=10, null=True, blank=True)
    pH_inicial = models.CharField(max_length=10, null=True, blank=True)
    pH_final = models.CharField(max_length=10, null=True, blank=True)
    observaciones = models.TextField(max_length=100, null=True, blank=True)


class SeguimientoFermentacion(CreationModificationDateMixin):
    """
    Proceso de control de Fermentacion,
    se distingue todo el proceso por un ID unico, el lote_nro
    """
    class Meta:
        verbose_name = "Seguimiento de Fermentacion"
        verbose_name_plural = "Seguimientos de Fermentacion"

    lote = models.OneToOneField(
        Lote, on_delete=models.CASCADE, primary_key=True)
    #fecha_inicio = models.DateField(null=True, blank=True)
    vasija = models.CharField(max_length=10, null=True, blank=True)
    fecha_llenado = models.DateField(null=True, blank=True)
    litros = models.FloatField(null=True, blank=True)
    fecha_inoculacion_levadura = models.DateField(null=True, blank=True)
    tipo_levadura = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(f"Planilla de Control de Fermentación - Lote número {self.lote.lote_nro}")


class InoculacionLevadura(models.Model):
    """
    Podría estar incluida en la misma Clase de seguimiento de Fermentación,
    pero se separa por su cantidad de atributos
    """
    class Meta:
        verbose_name = "Inoculación de Levadura"
        verbose_name_plural = "Inoculaciones de Levadura"

    seguimiento_control_fermentacion = models.OneToOneField(
        SeguimientoFermentacion, on_delete=models.CASCADE)
    hora = models.TimeField(
        choices=constants.HORA, null=True, blank=True)
    levadura = models.CharField(max_length=20, null=True, blank=True)
    dosis = models.CharField(
        help_text="(g/Hl)", max_length=20, null=True, blank=True)
    temp_sala = models.CharField(
        help_text="grados Centígrados", max_length=10, null=True, blank=True)
    temp_mosto = models.CharField(
        help_text="grados Centígrados", max_length=10, null=True, blank=True)
    densidad = models.CharField(max_length=20, null=True, blank=True)
    observaciones = models.TextField(max_length=100, null=True, blank=True)


class RegistroFermentacion(models.Model):

    class Meta:
        verbose_name = "Registro de Fermentación"
        verbose_name_plural = "Registros de Fermentación"

    seguimiento_control_fermentacion = models.ForeignKey(
        'SeguimientoFermentacion', on_delete=models.CASCADE, null=True)
    fecha = models.DateField(null=True, blank=True)
    hora = models.TimeField(
        choices=constants.HORA, null=True, blank=True)
    densidad = models.CharField(max_length=20, null=True, blank=True)
    temp_sala = models.CharField(
        help_text="grados Centígrados", max_length=10, null=True, blank=True)
    temp_mosto = models.CharField(
        help_text="grados Centígrados", max_length=10, null=True, blank=True)
    pH = models.CharField(max_length=20, null=True, blank=True)
    observaciones = models.TextField(
        max_length=100, null=True, blank=True)


# PLANILLA CONTROL DE CLARIFICACION / FILTRACION

class SeguimientoClarificacionFiltracion(CreationModificationDateMixin):
    """
    Proceso de control de Clarificación/Filtración,
    se distingue todo el proceso por un ID unico, el lote_nro
    """
    class Meta:
        verbose_name = "Seguimiento Clarificación y Filtración"
        verbose_name_plural = "Seguimientos de Clarificación y Filtración"

    lote = models.OneToOneField(
        Lote, on_delete=models.CASCADE, primary_key=True)
    placa_tipo = models.CharField(max_length=10, null=True, blank=True)
    placa_cantidad = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return str(f"Planilla de Control de Clarificación/Filtración - Lote número {self.lote.lote_nro}")


class RegistroClarificacionFiltracion(models.Model):

    class Meta:
        ordering = ["orden"]
        verbose_name = "Registro Clarificación y Filtración"
        verbose_name_plural = "Registros de Clarificación y Filtración"

    seguimiento_control_clarificacion_filtracion = models.ForeignKey(
        'SeguimientoClarificacionFiltracion',
        on_delete=models.CASCADE, null=True)
    orden = models.PositiveIntegerField()
    origen = models.CharField(max_length=20, null=True, blank=True)
    # WIP, Debe ser cambiado a FK a clase barril
    destino_barril = models.ForeignKey('Barril',
                                       on_delete=models.CASCADE, null=True)
    hora_inicio = models.TimeField(
        choices=constants.HORA, null=True, blank=True)
    kg_fin = models.FloatField(null=True, blank=True)
    presion_filtro = models.CharField(max_length=10, null=True, blank=True)
    observaciones = models.TextField(
        max_length=100, help_text="Turbidez", null=True, blank=True)


# PLANILLA CONTROL DE CARBONATACION

class SeguimientoCarbonatacion(CreationModificationDateMixin):
    """
    Tercer seguimiento de la elaboración,
    se distingue todo el suiemiento por un ID único, el lote_nro
    """

    fecha_fin = models.DateField(null=True, blank=True)
    lote = models.OneToOneField(
        Lote, on_delete=models.CASCADE, primary_key=True)
    observaciones = models.TextField(
        max_length=100, null=True, blank=True)

    def __str__(self):
        return str(f"Planilla de Carbonatación - Lote número {self.lote.lote_nro}")
