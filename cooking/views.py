from django.shortcuts import render
from .models import Lote, SeguimientoMaceracionCoccion, Maceracion, Correccion, OllaMaceracion, OllaAguaCaliente, EtapaOllaAguaCaliente, Coccion, EtapaCoccion, Adicion, SeguimientoFermentacionClarificacion, SeguimientoCarbonatacion
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse



# Create your views here.
@login_required
def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    return render(
        request,
        'index.html'
    )

class LoteView(LoginRequiredMixin,ListView):
    """
    vista genérica basada en clases para listar lotes 
    """
    model = Lote
    paginate_by = 10
    context_object_name = 'lotes'
    template_name = 'lotelist.html'

class LoteSeguimientosView(LoginRequiredMixin,DetailView):
    """
    VBC que lista todos los procesos creados para un lote en particular
    """
    model = Lote
    template_name = 'lote_seguimientos.html'

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    #    context['seguimientos'] = [SeguimientoMaceracionCoccion.objects.filter(lote=self.object), SeguimientoFermentacionClarificacion.objects.filter(lote=self.object), SeguimientoCarbonatacion.objects.filter(lote=self.object)]
        context['seguimiento_maceracion_coccion'] = SeguimientoMaceracionCoccion.objects.filter(lote=self.object)
        context['seguimiento_fermentacion_clarificacion'] = SeguimientoFermentacionClarificacion.objects.filter(lote=self.object)
        context['seguimiento_carbonatacion'] = SeguimientoCarbonatacion.objects.filter(lote=self.object)

        return context
    pass


class LoteCreate(LoginRequiredMixin,CreateView):
    model = Lote
    fields = '__all__'
    def get_success_url(self):
        return reverse('lotelist')
