from django.shortcuts import render
from .models import Lote, ProcesoMaceracionCoccion, Maceracion, Correccion, OllaMaceracion, OllaAguaCaliente, EtapaOllaAguaCaliente, Coccion, EtapaCoccion, Adicion
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

