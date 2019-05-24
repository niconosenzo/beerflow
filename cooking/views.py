from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .multiple_forms import MultipleFormsView
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
        # self.object = self.get_object()
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)
        if self.request.POST:
            # context['form'] = form
            context['olla_maceracion_form_set'] = OllaMaceracionFormset(self.request.POST, instance=self.object)
            context['correccion_form_set'] = CorreccionFormset(self.request.POST, instance=self.object)
            context['olla_agua_caliente_form_set'] = OllaAguaCalienteFormset(self.request.POST, instance=self.object)
        else:
            context['olla_maceracion_form_set'] = OllaMaceracionFormset(instance=self.object)
            context['correccion_form_set'] = CorreccionFormset( instance=self.object)
            context['olla_agua_caliente_form_set'] = OllaAguaCalienteFormset( instance=self.object)
        # if 'form' not in context:
        #     context['form'] = self.form_class(initial={'some_field': context['model'].some_field})
        # if 'form2' not in context:
        #     context['form2'] = self.second_form_class(initial={'another_field': context['model'].another_field})
        return context

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #
    #
    #     # formset Correccion
    #     correcciones = Correccion.objects.filter(maceracion=self.object).order_by('pk')
    #     correcciones_data = []
    #     for correccion in correcciones:
    #         d = {'inicial': correccion.inicial,
    #             'acido_fosforico': correccion.acido_fosforico,
    #             'final_maceracion': correccion.final_maceracion}
    #         correcciones_data.append(d)
    #     correccion_form_set = CorreccionFormset(initial=correcciones_data)
    #
    #     # formset olla maceracion
    #     olla_maceraciones = OllaMaceracion.objects.filter(maceracion=self.object).order_by('pk')
    #     olla_maceraciones_data = []
    #     for olla_maceracion in olla_maceraciones:
    #         e = {'granos': olla_maceracion.granos,
    #             'cantidad': olla_maceracion.cantidad,
    #             'agua': olla_maceracion.agua}
    #         olla_maceraciones_data.append(e)
    #     olla_maceracion_form_set = OllaMaceracionFormset(initial=olla_maceraciones_data)
    #
    #     # formset olla agua caliente
    #     # olla_calientes = OllaAguaCaliente.objects.filter(maceracion=self.object).order_by('pk')
    #     # olla_calientes_data = []
    #     # for olla_caliente in olla_calientes:
    #     #     o = {'agua_dureza': olla_caliente.agua_dureza,
    #     #          'agua_ph': olla_caliente.agua_ph,
    #     #          'filtracion_hora_inicio': olla_caliente.filtracion_hora_inicio}
    #     #     olla_calientes_data.append(o)
    #     # olla_agua_caliente_form_set = OllaAguaCalienteFormset(initial=olla_calientes_data)
    #     # olla_caliente = OllaAguaCaliente.objects.get(maceracion=self.object)
    #     olla_agua_caliente_form_set = OllaAguaCalienteFormset(instance=self.object)
    #     return self.render_to_response(self.get_context_data(form=form,
    #                                                          correccion_form_set=correccion_form_set,
    #                                                          olla_maceracion_form_set=olla_maceracion_form_set,
    #                                                          olla_agua_caliente_form_set=olla_agua_caliente_form_set))

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     correccion_form_set = CorreccionFormset(request.POST)
    #     olla_maceracion_form_set = OllaMaceracionFormset(request.POST)
    #     olla_agua_caliente_form_set = OllaAguaCalienteFormset(request.POST)
    #
    #     if form.is_valid() and correccion_form_set.is_valid() and olla_maceracion_form_set.is_valid() and olla_agua_caliente_form_set.is_valid():
    #         return self.form_valid(form, correccion_form_set,
    #                                olla_maceracion_form_set,
    #                                olla_agua_caliente_form_set)
    #     else:
    #         return self.form_invalid(form, correccion_form_set,
    #                                  olla_maceracion_form_set,
    #                                  olla_agua_caliente_form_set)



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

    # def form_valid(self, form, correccion_form_set, olla_maceracion_form_set, olla_agua_caliente_form_set):
    #
    #     self.object = form.save()
    #
    #     #correccion formset
    #     correccion_form_set.instance = self.object
    #     #Correccion.objects.filter(maceracion=self.object).delete()
    #     correccion_form_set.save()
    #
    #     # olla maceracion formset
    #     olla_maceracion_form_set.instance = self.object
    #     #OllaMaceracion.objects.filter(maceracion=self.object).delete()
    #     olla_maceracion_form_set.save()
    #
    #     # olla caliente formset
    #     olla_agua_caliente_form_set.instance = self.object
    #     #OllaAguaCaliente.objects.filter(maceracion=self.object).delete()
    #     olla_agua_caliente_form_set.save()
    #     print(self.forms)
    #
    #     return HttpResponseRedirect(self.get_success_url())

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

    olla_maceracion_batch1 = OllaMaceracion(maceracion=maceracion_batch1)
    olla_maceracion_batch1.save()

    olla_maceracion_batch2 = OllaMaceracion(maceracion=maceracion_batch2)
    olla_maceracion_batch2.save()

    olla_agua_caliente_batch1 = OllaAguaCaliente(maceracion=maceracion_batch1)
    olla_agua_caliente_batch1.save()

    olla_agua_caliente_batch2 = OllaAguaCaliente(maceracion=maceracion_batch2)
    olla_agua_caliente_batch2.save()

    etapa_olla_agua_caliente_batch1 = EtapaOllaAguaCaliente(olla_agua_caliente=olla_agua_caliente_batch1)
    etapa_olla_agua_caliente_batch1.save()

    etapa_olla_agua_caliente_batch2 = EtapaOllaAguaCaliente(olla_agua_caliente=olla_agua_caliente_batch2)
    etapa_olla_agua_caliente_batch2.save()

    ## coccion
    coccion_batch1 = Coccion(batch_nro=1,
                    proceso_maceracion_coccion=seguimiento_maceracion_coccion)
    coccion_batch2 = Coccion(batch_nro=2,
                    proceso_maceracion_coccion=seguimiento_maceracion_coccion)
    coccion_batch1.save()
    coccion_batch2.save()
    return HttpResponseRedirect(reverse('lote_seguimientos_list',
                                kwargs={'pk': pk}))
