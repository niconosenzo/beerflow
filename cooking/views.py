from django.shortcuts import render, get_object_or_404
from .models import Lote, SeguimientoMaceracionCoccion, Maceracion, Correccion, OllaMaceracion, OllaAguaCaliente, EtapaOllaAguaCaliente, Coccion, EtapaCoccion, Adicion, SeguimientoFermentacionClarificacion, SeguimientoCarbonatacion
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import PlanillaMaceracionCoccion


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

    # sear bar
    def get_queryset(self):
        if self.request.GET.get("q"):
            queryset = Lote.objects.filter(lote_nro__icontains=self.request.GET.get("q"))
            return queryset

        return Lote.objects.all()

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
        context['lote'] = self.object

        return context


class LoteCreate(LoginRequiredMixin,CreateView):
    model = Lote
    fields = '__all__'
    def get_success_url(self):
        return reverse('lote_seguimientos_list',  kwargs={'pk':self.object.lote_nro})

# formulario Planilla de Maceracion / Coccion
def SeguimientoMaceracionCoccionUpdate(request, pk):

    seguimiento_maceracion_coccion = get_object_or_404(SeguimientoMaceracionCoccion,lote = Lote.objects.get(lote_nro=pk))
    print(f"IIIIIIIMPRIENDOOOO {seguimiento_maceracion_coccion.lote.lote_nro}")

    # check if this is a POST request, if so, process the form
    if request.method == 'POST':
        print("lalalala POST POST POST")
    else:
        # it's a GET request
        values = {
            "lote": seguimiento_maceracion_coccion.lote.lote_nro,
            "fecha_inicio": seguimiento_maceracion_coccion.fecha_inicio,
            "fecha_fin": seguimiento_maceracion_coccion.fecha_fin,
            "observaciones": seguimiento_maceracion_coccion.observaciones,

        }
        initial = dict(values)
        form = PlanillaMaceracionCoccion(initial)

    return render(request, 'cooking/planillaMC.html', {'form': form})

@login_required
def SeguimientoMaceracionCoccionCreate(request, pk):
    # Creamos todos los objectos necesarios para la planilla a partir del lote_nro (pk)
    ## seguimiento maceracion
    seguimiento_maceracion_coccion = SeguimientoMaceracionCoccion(lote=Lote.objects.get(lote_nro=pk))
    seguimiento_maceracion_coccion.save()

   ## maceracion
    maceracion_batch1 = Maceracion(batch_nro=1,seguimiento_maceracion_coccion=seguimiento_maceracion_coccion)
    maceracion_batch2 = Maceracion(batch_nro=2,seguimiento_maceracion_coccion=seguimiento_maceracion_coccion)
    maceracion_batch1.save()
    maceracion_batch2.save()

    ## olla maceracion
    olla_maceracion1 = OllaMaceracion(maceracion=maceracion_batch1)
    olla_maceracion2 = OllaMaceracion(maceracion=maceracion_batch2)

    return HttpResponseRedirect(reverse('lote_seguimientos_list',  kwargs={'pk':pk}))
