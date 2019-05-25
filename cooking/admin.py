from django.contrib import admin
from .models import Lote, SeguimientoMaceracionCoccion, Maceracion, Correccion, OllaMaceracion, OllaAguaCaliente, EtapaOllaAguaCaliente, Coccion, EtapaCoccion, SeguimientoFermentacionClarificacion, SeguimientoCarbonatacion

admin.site.register(Lote)
admin.site.register(SeguimientoMaceracionCoccion)
admin.site.register(Maceracion)
admin.site.register(Correccion)
admin.site.register(OllaMaceracion)
admin.site.register(OllaAguaCaliente)
admin.site.register(EtapaOllaAguaCaliente)
admin.site.register(Coccion)
admin.site.register(EtapaCoccion)
admin.site.register(SeguimientoFermentacionClarificacion)
admin.site.register(SeguimientoCarbonatacion)

# Register your models here.
