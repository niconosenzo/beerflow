from .models import *
import datetime


def init_planilla_MaceracionCoccion(pk):
    """
     Inicializamos la planilla, creando
     todos los  objectos necesarios para la planilla
     a partir del lote_nro (pk)
     """
    ## seguimiento maceracion
    seguimiento_maceracion_coccion = SeguimientoMaceracionCoccion(
                                    lote=Lote.objects.get(lote_nro=pk),
                                    fecha_inicio=datetime.date.today())
    seguimiento_maceracion_coccion.save()

    ## maceracion
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

    etapa_olla_agua_caliente_batch1 = EtapaOllaAguaCaliente(olla_agua_caliente=olla_agua_caliente_batch1)
    etapa_olla_agua_caliente_batch1.save()

    etapa_olla_agua_caliente_batch2 = EtapaOllaAguaCaliente(olla_agua_caliente=olla_agua_caliente_batch2)
    etapa_olla_agua_caliente_batch2.save()

    ## coccion
    coccion_batch1 = Coccion(batch_nro=1,
                    proceso_maceracion_coccion=seguimiento_maceracion_coccion)
    coccion_batch2 = Coccion(batch_nro=2,
                    proceso_maceracion_coccion=seguimiento_maceracion_coccion)
    coccion_batch1.save()
    coccion_batch2.save()
    pass
