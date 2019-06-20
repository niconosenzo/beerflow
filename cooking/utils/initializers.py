from ..models import *
import datetime


def init_planilla_MaceracionCoccion(pk):
    """
     Inicializamos la planilla, creando
     todos los  objectos necesarios para la planilla
     a partir del lote_nro (pk)
     """
    # seguimiento maceracion
    seguimiento_maceracion_coccion = SeguimientoMaceracionCoccion(
        lote=Lote.objects.get(lote_nro=pk))
    seguimiento_maceracion_coccion.save()

    # maceracion
    maceracion_batch1 = Maceracion(batch_nro=1,
                                   seguimiento_maceracion_coccion=seguimiento_maceracion_coccion)
    maceracion_batch1.save()

    correccion_batch1 = Correccion(maceracion=maceracion_batch1)
    correccion_batch1.save()

    maceracion_batch2 = Maceracion(batch_nro=2,
                                   seguimiento_maceracion_coccion=seguimiento_maceracion_coccion)
    maceracion_batch2.save()

    correccion_batch2 = Correccion(maceracion=maceracion_batch2)
    correccion_batch2.save()

    olla_maceracion_batch1 = OllaMaceracion(maceracion=maceracion_batch1)
    olla_maceracion_batch1.save()

    olla_maceracion_batch2 = OllaMaceracion(maceracion=maceracion_batch2)
    olla_maceracion_batch2.save()

    olla_agua_caliente_batch1 = OllaAguaCaliente(maceracion=maceracion_batch1)
    olla_agua_caliente_batch1.save()

    olla_agua_caliente_batch2 = OllaAguaCaliente(maceracion=maceracion_batch2)
    olla_agua_caliente_batch2.save()

    etapa_olla_agua_caliente_batch1 = EtapaOllaAguaCaliente(
        olla_agua_caliente=olla_agua_caliente_batch1)
    etapa_olla_agua_caliente_batch1.save()

    etapa_olla_agua_caliente_batch2 = EtapaOllaAguaCaliente(
        olla_agua_caliente=olla_agua_caliente_batch2)
    etapa_olla_agua_caliente_batch2.save()

    # coccion
    coccion_batch1 = Coccion(batch_nro=1,
                             proceso_maceracion_coccion=seguimiento_maceracion_coccion)
    coccion_batch2 = Coccion(batch_nro=2,
                             proceso_maceracion_coccion=seguimiento_maceracion_coccion)
    coccion_batch1.save()
    coccion_batch2.save()

   # para el batch 1:
    for etapa in [i[0] for i in EtapaCoccion.NOMBRE_ETAPA]:
        # creamos las etapas individualmente
        etapatemp = EtapaCoccion(coccion=coccion_batch1, etapa_nombre=etapa)
        etapatemp.save()

    adicion1 = AdicionCoccion(coccion=coccion_batch1)
    adicion1.save()

    # para el batch 2
    for etapa in [i[0] for i in EtapaCoccion.NOMBRE_ETAPA]:
        # creamos las etapas individualmente
        etapatemp = EtapaCoccion(coccion=coccion_batch2, etapa_nombre=etapa)
        etapatemp.save()

    adicion2 = AdicionCoccion(coccion=coccion_batch2)
    adicion2.save()

    pass


def init_planilla_Fermentacion(pk):
    # seguimiento fermentacion
    seguimiento_fermentacion = SeguimientoFermentacion(
        lote=Lote.objects.get(lote_nro=pk))
    seguimiento_fermentacion.save()

    # parametros fundamentales
    parametros_fundamentales = ParametrosFundamentales(
        lote=Lote.objects.get(lote_nro=pk))
    parametros_fundamentales.save()

    # inoculación levadura
    inoculacion_levadura = InoculacionLevadura(
        seguimiento_control_fermentacion=seguimiento_fermentacion)
    inoculacion_levadura.save()

    # registro fermentacion
    registro_fermentacion = RegistroFermentacion(
        seguimiento_control_fermentacion=seguimiento_fermentacion)
    registro_fermentacion.save()
    pass


def init_planilla_Clarificacion_Filtracion(pk):
    # seguimiento clarificacion filtracion
    seguimiento_clarificacion_filtracion = SeguimientoClarificacionFiltracion(
        lote=Lote.objects.get(lote_nro=pk))
    seguimiento_clarificacion_filtracion.save()

    # registro clarificacion filtracion
    for orden in range(1, 11):
        registro_clarificacion = RegistroClarificacionFiltracion(
            seguimiento_control_clarificacion_filtracion=seguimiento_clarificacion_filtracion,
            orden=orden)
        registro_clarificacion.save()
    pass
