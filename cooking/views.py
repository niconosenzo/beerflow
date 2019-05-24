from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import *
from .initializers import init_planilla_MaceracionCoccion


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


class BatchMaceracionCoccionlist(LoginRequiredMixin, UpdateView):
    """
    VBC que lista primer y segundo Batch tanto para maceracion
     como para coccion
    """
    model = SeguimientoMaceracionCoccion
    template_name = 'seguimientos_batch.html'
    form_class = SeguimientoMaceracionCoccionModelForm

    def get_success_url(self):
        print(self.kwargs.get("slug"))
        return reverse('batch_maceracion_coccion_list',
                       kwargs={'pk': self.object.lote.lote_nro})


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


class LoteCreate(LoginRequiredMixin, CreateView):
    model = Lote
    form_class = LoteModelForm

    def get_success_url(self):
        return reverse('lote_seguimientos_list',
                       kwargs={'pk': self.object.lote_nro})


class MaceracionUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'planilla_maceracion_coccion.html'
    form_class = MaceracionModelForm
    model = Maceracion

    forms_classes = [
        MaceracionModelForm,
        CorreccionFormset,
        OllaMaceracionFormset,
        OllaAguaCalienteFormset
    ]

    def get_object(self, **kwargs):
        return get_object_or_404(Maceracion, seguimiento_maceracion_coccion=SeguimientoMaceracionCoccion.objects.get(lote=Lote.objects.get(lote_nro=self.kwargs.get("pk"))), batch_nro=self.kwargs.get("batch"))


    def get_success_url(self):
        return reverse('maceracion_update',
                kwargs={'pk': self.object.seguimiento_maceracion_coccion.lote.lote_nro, 'batch': self.object.batch_nro})


    def get_context_data(self, **kwargs):
        context = super(MaceracionUpdate, self).get_context_data(**kwargs)

        if self.request.POST:
            # context['form'] = form
            context['olla_maceracion_form_set'] = OllaMaceracionFormset(self.request.POST, instance=self.object)
            context['correccion_form_set'] = CorreccionFormset(self.request.POST, instance=self.object)
            context['olla_agua_caliente_form_set'] = OllaAguaCalienteFormset(self.request.POST, instance=self.object)
        else:
            context['olla_maceracion_form_set'] = OllaMaceracionFormset(instance=self.object)
            context['correccion_form_set'] = CorreccionFormset( instance=self.object)
            context['olla_agua_caliente_form_set'] = OllaAguaCalienteFormset( instance=self.object)
        return context



    def form_valid(self, form):
        context = self.get_context_data()
        olla_maceracion_form_set = context['olla_maceracion_form_set']
        correccion_form_set = context['correccion_form_set']
        olla_agua_caliente_form_set = context['olla_agua_caliente_form_set']
        self.object = form.save()

        form.instance.created_by = self.request.user
        self.object = form.save()
        if olla_maceracion_form_set.is_valid():
            olla_maceracion_form_set.instance = self.object
            olla_maceracion_form_set.save()
        if correccion_form_set.is_valid():
            correccion_form_set.instance = self.object
            correccion_form_set.save()
        if olla_agua_caliente_form_set.is_valid():
            olla_agua_caliente_form_set.instance = self.object
            olla_agua_caliente_form_set.save()

        return super(MaceracionUpdate, self).form_valid(form)



    def form_invalid(self, form, correccion_form_set,
                     olla_maceracion_form_set,
                     olla_agua_caliente_form_set):
        return self.render_to_response(self.get_context_data(form=form,
                                                             correccion_form_set=correccion_form_set,
                                                             olla_maceracion_form_set=olla_maceracion_form_set,
                                                             olla_agua_caliente_form_set=olla_agua_caliente_form_set))


class CoccionUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'planilla_maceracion_coccion.html'
    form_class = CoccionModelForm
    model = Coccion

    def get_object(self, **kwargs):
        return get_object_or_404(Coccion, proceso_maceracion_coccion=SeguimientoMaceracionCoccion.objects.get(lote=Lote.objects.get(lote_nro=self.kwargs.get("pk"))), batch_nro=self.kwargs.get("batch"))

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('coccion_update',
                kwargs={'pk': self.object.proceso_maceracion_coccion.lote.lote_nro, 'batch': self.object.batch_nro})



@login_required
def SeguimientoMaceracionCoccionCreate(request, pk):
    """
     Inicializamos la planilla, creando
     todos los  objectos necesarios para la planilla
     a partir del lote_nro (pk)
     """
    init_planilla_MaceracionCoccion(pk)
    return HttpResponseRedirect(reverse('lote_seguimientos_list',
                                kwargs={'pk': pk}))
