from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView,FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.forms.models import inlineformset_factory
from .forms import *
import time, datetime


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


class LoteView(LoginRequiredMixin, ListView):
    """
    vista genérica basada en clases para listar lotes
    """
    model = Lote
    paginate_by = 10
    context_object_name = 'lotes'
    template_name = 'lotelist.html'

    # search bar
    def get_queryset(self):
        if self.request.GET.get("q"):
            queryset = Lote.objects.filter(
                lote_nro__icontains=self.request.GET.get("q"))
            return queryset

        return Lote.objects.all()


class BatchMaceracionCoccionlist(LoginRequiredMixin, DetailView):
    """
    VBC que lista primer y segundo Batch tanto para maceracion
     como para coccion
    """
    model = SeguimientoMaceracionCoccion
    template_name = 'seguimientos_batch.html'


class LoteSeguimientosView(LoginRequiredMixin, DetailView):
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
        return reverse('lote_seguimientos_list',
                       kwargs={'pk': self.object.lote_nro})


class MaceracionCoccionUpdate(LoginRequiredMixin, UpdateView):
    model = SeguimientoMaceracionCoccion
    template_name = 'planilla_maceracion_coccion.html'
    form_class = SeguimientoMaceracionCoccionModelForm


    def get_context_data(self, **kwargs):
        data = super(MaceracionCoccionUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['maceraciones'] = MaceracionCoccionFormSet(self.request.POST, instance=self.object)
        else:
            data['maceraciones'] = MaceracionCoccionFormSet(instance=self.object)
        return data


    def get_success_url(self):
        return reverse_lazy('maceracion_coccion_update',
                       kwargs={'pk': self.object.lote.lote_nro})


    def form_valid(self, form):
        context = self.get_context_data()
        maceraciones = context['maceraciones']
    #    with self.transaction.atomic():
        form.instance.created_by = self.request.user
        self.object = form.save()
        if maceraciones.is_valid():
            maceraciones.instance = self.object
            maceraciones.save()
        return super(MaceracionCoccionUpdate, self).form_valid(form)

    class CollectionDelete(DeleteView):
        model = Maceracion
        template_name = 'confirm_delete.html'
        success_url = reverse_lazy('lotelist')



@login_required
def SeguimientoMaceracionCoccionCreate(request, pk):
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

    ## coccion
    cocccion_batch1 = Coccion(batch_nro=1,
                    proceso_maceracion_coccion=seguimiento_maceracion_coccion)
    cocccion_batch2 = Coccion(batch_nro=2,
                    proceso_maceracion_coccion=seguimiento_maceracion_coccion)
    cocccion_batch1.save()
    cocccion_batch2.save()
    return HttpResponseRedirect(reverse('lote_seguimientos_list',
                                kwargs={'pk': pk}))
