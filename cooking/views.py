from django.shortcuts import render
from .models import Lote, SeguimientoMaceracionCoccion, Maceracion, Correccion, OllaMaceracion, OllaAguaCaliente, EtapaOllaAguaCaliente, Coccion, EtapaCoccion, Adicion, SeguimientoFermentacionClarificacion, SeguimientoCarbonatacion
from django.views.generic import ListView, DetailView


# Create your views here.

def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    return render(
        request,
        'index.html'
    )

class LoteView(ListView):
    """
    vista genérica basada en clases para listar lotes 
    """
    model = Lote
    paginate_by = 10
    context_object_name = 'lotes'
    template_name = 'lotelist.html'

class LoteSeguimientosView(DetailView):
    """
    VBC que lista todos los procesos creados para un lote en particular
    """
    model = Lote
    template_name = 'lote_seguimientos.html'

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['seguimiento_maceracion_coccion'] = SeguimientoMaceracionCoccion.objects.filter(lote=self.object)
        context['seguimiento_fermentacion_clarificacion'] = SeguimientoFermentacionClarificacion.objects.filter(lote=self.object)
        context['seguimiento_carbonatacion'] = SeguimientoCarbonatacion.objects.filter(lote=self.object)

        return context
    pass
