from django.shortcuts import render
from .models import Lote, SeguimientoMaceracionCoccion, Maceracion, Correccion, OllaMaceracion, OllaAguaCaliente, EtapaOllaAguaCaliente, Coccion, EtapaCoccion, Adicion, SeguimientoFermentacionClarificacion, SeguimientoCarbonatacion
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.forms import ModelForm


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
        context['seguimientos'] = [SeguimientoMaceracionCoccion.objects.filter(lote=self.object), SeguimientoFermentacionClarificacion.objects.filter(lote=self.object), SeguimientoCarbonatacion.objects.filter(lote=self.object)]
        context['seguimiento_maceracion_coccion'] = SeguimientoMaceracionCoccion.objects.filter(lote=self.object)
        context['seguimiento_fermentacion_clarificacion'] = SeguimientoFermentacionClarificacion.objects.filter(lote=self.object)
        context['seguimiento_carbonatacion'] = SeguimientoCarbonatacion.objects.filter(lote=self.object)

        return context
    pass


class LoteCreate(LoginRequiredMixin,CreateView):
    model = Lote
    fields = '__all__'
    def get_success_url(self):
        print(self.object.__dict__)
        return reverse('lote_seguimientos_list',  kwargs={'pk':self.object.lote_nro})

#class LoteCreate(LoginRequiredMixin, ModelForm):
#    model = Lote
#    fields = '__all__'
#    class Meta:
#        model = Lote
#        fields = '__all__'
#
#    def get_success_url(self):
#        return reverse('lote_seguimientos_list', pk=self.cleaned_data['lote_nro'])
