from django.contrib import admin
from .models import Lote, ProcesoMaceracionCoccion, Maceracion, Correccion, OllaMaceracion, OllaAguaCaliente, EtapaOllaAguaCaliente, Coccion, EtapaCoccion, Adicion

admin.site.register(Lote)
admin.site.register(ProcesoMaceracionCoccion)
admin.site.register(Maceracion)
admin.site.register(Correccion)
admin.site.register(OllaMaceracion)
admin.site.register(OllaAguaCaliente)
admin.site.register(EtapaOllaAguaCaliente)
admin.site.register(Coccion)
admin.site.register(EtapaCoccion)
admin.site.register(Adicion)

# Register your models here.
