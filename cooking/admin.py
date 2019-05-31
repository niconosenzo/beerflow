from django.contrib import admin
from .models import (
    Lote,
    SeguimientoMaceracionCoccion,
    Maceracion,
    Correccion,
    OllaMaceracion,
    OllaAguaCaliente,
    EtapaOllaAguaCaliente,
    Coccion,
    EtapaCoccion,
    SeguimientoFermentacion,
    SeguimientoCarbonatacion,
    SeguimientoClarificacionFiltracion,
    ParametrosFundamentales,
    InoculacionLevadura,
    RegistroFermentacion,
    AdicionCoccion,
    RegistroClarificacionFiltracion
)

admin.site.register(Lote)
admin.site.register(SeguimientoMaceracionCoccion)
admin.site.register(Maceracion)
admin.site.register(Correccion)
admin.site.register(OllaMaceracion)
admin.site.register(OllaAguaCaliente)
admin.site.register(EtapaOllaAguaCaliente)
admin.site.register(Coccion)
admin.site.register(EtapaCoccion)
admin.site.register(SeguimientoFermentacion)
admin.site.register(SeguimientoClarificacionFiltracion)
admin.site.register(ParametrosFundamentales)
admin.site.register(InoculacionLevadura)
admin.site.register(RegistroFermentacion)
admin.site.register(RegistroClarificacionFiltracion)
admin.site.register(SeguimientoCarbonatacion)
admin.site.register(AdicionCoccion)

# Register your models here.
