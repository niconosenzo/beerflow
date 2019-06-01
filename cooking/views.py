from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import *
from .initializers import (
    init_planilla_MaceracionCoccion,
    init_planilla_Fermentacion)
from django.contrib import messages


# Create your views here.
@login_required
def index(request):
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


class BarrilView(LoginRequiredMixin, ListView):
    """
    vista genérica basada en clases para listar barriles
    """
    model = Barril
    paginate_by = 10
    context_object_name = 'barriles'
    template_name = 'barrillist.html'

    # search bar
    def get_queryset(self):
        if self.request.GET.get("q"):
            queryset = Barril.objects.filter(
                barril_nro__icontains=self.request.GET.get("q"))
            return queryset

        return Barril.objects.all()


class MovimientosBarrilView(LoginRequiredMixin, ListView):
    """
    vista genérica basada en clases para listar movimientos de barriles
    """
    model = MovimientosBarril
    paginate_by = 10
    context_object_name = 'movimientos'
    template_name = 'movimientoslist.html'

    # search bar
    def get_queryset(self):
        if self.request.GET.get("q"):
            queryset = MovimientosBarril.objects.filter(
                barril__barril_nro__icontains=self.request.GET.get("q"))
            return queryset

        if self.request.GET.get("l"):
            queryset = MovimientosBarril.objects.filter(
                lote__lote_nro__icontains=self.request.GET.get("l"))
            return queryset
        return MovimientosBarril.objects.all()


class UpdateMovimientosBarrilView(LoginRequiredMixin, UpdateView):
    model = MovimientosBarril
    form_class = MovimientosBarrilModelForm
    template_name = 'movimientos_form.html'

    def get_success_url(self):
        return reverse('movimientoslist')


class LoteMovimientosBarrilView(LoginRequiredMixin, ListView):
    """
    vista genérica basada en clases para listar movimientos
    para un lote determinado
    """
    model = MovimientosBarril
    paginate_by = 10
    context_object_name = 'movimientos'
    template_name = 'movimientoslist.html'

    def get_queryset(self):
        queryset = MovimientosBarril.objects.filter(
            lote__lote_nro__icontains=self.kwargs['lote'])
        return queryset


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

    def get_context_data(self, **kwargs):
        context = super(BatchMaceracionCoccionlist,
                        self).get_context_data(**kwargs)

        context['pk'] = self.kwargs.get("pk")
        return context


class LoteSeguimientosView(LoginRequiredMixin, DetailView):
    """
    VBC que lista todos los procesos creados para un lote en particular
    """
    model = Lote
    template_name = 'lote_seguimientos.html'

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['seguimientos'] = [SeguimientoMaceracionCoccion.objects.filter(lote=self.object), SeguimientoFermentacion.objects.filter(
            lote=self.object), SeguimientoClarificacionFiltracion.objects.filter(lote=self.object), SeguimientoCarbonatacion.objects.filter(lote=self.object)]
        context['seguimiento_maceracion_coccion'] = SeguimientoMaceracionCoccion.objects.filter(
            lote=self.object)
        context['seguimiento_fermentacion'] = SeguimientoFermentacion.objects.filter(
            lote=self.object)
        context['seguimiento_clarificacion_filtracion'] = SeguimientoClarificacionFiltracion.objects.filter(
            lote=self.object)
        context['seguimiento_carbonatacion'] = SeguimientoCarbonatacion.objects.filter(
            lote=self.object)
        context['lote'] = self.object

        return context


class LoteCreate(LoginRequiredMixin, CreateView):
    model = Lote
    form_class = LoteModelForm
    template_name = 'lote_form.html'

    def get_success_url(self):
        return reverse('lote_seguimientos_list',
                       kwargs={'pk': self.object.lote_nro})


class BarrilCreate(LoginRequiredMixin, CreateView):
    model = Barril
    form_class = BarrilModelForm
    template_name = 'barril_form.html'

    def get_success_url(self):
        return reverse('barrillist')
        # kwargs={'pk': self.object.lote_nro})


class MovimientosBarrilCreate(LoginRequiredMixin, CreateView):
    model = MovimientosBarril
    form_class = MovimientosBarrilModelForm
    template_name = 'movimientos_form.html'

    def get_success_url(self):
        return reverse('movimientoslist')


class FermentacionUpdate(LoginRequiredMixin, UpdateView):
    """
    VBC que lista los datos de seguimiento de Fermentacion
    """
    model = SeguimientoFermentacion
    template_name = 'seguimientos_fermentacion.html'
    form_class = SeguimientoFermentacionModelForm

    def get_success_url(self):
        return reverse('fermentacion_list',
                       kwargs={'pk': self.object.lote.lote_nro})

    def get_context_data(self, **kwargs):
        context = super(FermentacionUpdate, self).get_context_data(**kwargs)
        object_parametros = ParametrosFundamentales.objects.get(
            lote=Lote.objects.get(lote_nro=self.kwargs.get("pk")))
        object_inoculacion = InoculacionLevadura.objects.get(
            seguimiento_control_fermentacion=SeguimientoFermentacion.objects.get(
                lote=Lote.objects.get(lote_nro=self.kwargs.get("pk"))))
        context['registro_fermentacion_form_set'] = RegistroFermentacionFormset(
            self.request.POST or None, instance=self.object)

        if self.request.POST:
            context['parametros_fundamentales'] = ParametrosFundamentalesModelForm(
                self.request.POST, instance=object_parametros)
            context['inoculacion_levadura'] = InoculacionLevaduraModelForm(
                self.request.POST or None, instance=object_inoculacion)
        else:
            context['parametros_fundamentales'] = ParametrosFundamentalesModelForm(initial={
                #    'lote': object_parametros.lote,
                'dO': object_parametros.dO,
                'dF': object_parametros.dF,
                'alcohol_teorico': object_parametros.alcohol_teorico,
                'pH_inicial': object_parametros.pH_inicial,
                'pH_final': object_parametros.pH_final,
                'observaciones': object_parametros.observaciones})

            context['inoculacion_levadura'] = InoculacionLevaduraModelForm(initial={
                'hora': object_inoculacion.hora,
                'levadura': object_inoculacion.levadura,
                'dosis': object_inoculacion.dosis,
                'temp_sala': object_inoculacion.temp_sala,
                'temp_mosto': object_inoculacion.temp_mosto,
                'densidad': object_inoculacion.densidad,
                'observaciones': object_inoculacion.observaciones})
        context['pk'] = self.kwargs.get("pk")
        return context
    #

    def get_object(self, **kwargs):
        return get_object_or_404(SeguimientoFermentacion, lote=Lote.objects.get(lote_nro=self.kwargs.get("pk")))

    def form_valid(self, form):
        context = self.get_context_data()
        parametros_fundamentales = context['parametros_fundamentales']
        inoculacion_levadura = context['inoculacion_levadura']
        registro_fermentacion_form_set = context['registro_fermentacion_form_set']
        print(form.errors)
        if form.is_valid():
            self.object = form.save()
            messages.success(self.request, 'Planilla Fermentación guardada')
        print(parametros_fundamentales.errors)
        if parametros_fundamentales.is_valid():
            pf = parametros_fundamentales.save(commit=False)
            pf.lote = Lote.objects.get(lote_nro=context['pk'])
            pf.save()
            messages.success(
                self.request, 'Parametros Fundamentales guardados')
        print(registro_fermentacion_form_set.errors)
        if registro_fermentacion_form_set.is_valid():
            registro_fermentacion_form_set.instance = self.object
            registro_fermentacion_form_set.save()
            messages.success(
                self.request, 'Registros de Fermentación guardados')
        print(inoculacion_levadura.errors)
        if inoculacion_levadura.is_valid():
            il = inoculacion_levadura.save(commit=False)
            il.lote = Lote.objects.get(lote_nro=context['pk'])
            il.save()
            messages.success(
                self.request, 'Inoculación de Levadura guardada')

        return super(FermentacionUpdate, self).form_valid(form)

    def form_invalid(self, form, parametros_fundamentales,
                     inoculacion_levadura,
                     registro_fermentacion_form_set):
        # def form_invalid(self, form):
        messages.error(self.request, 'Error al guardar.')
        # return self.render_to_response(self.get_context_data(form=form))
        return self.render_to_response(self.get_context_data(form=form,
                                                             parametros_fundamentales=parametros_fundamentales,
                                                             inoculacion_levadura=inoculacion_levadura,
                                                             registro_fermentacion_form_set=registro_fermentacion_form_set))


class MaceracionUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'planilla_maceracion_coccion.html'
    form_class = MaceracionModelForm
    model = Maceracion

    def get_object(self, **kwargs):
        return get_object_or_404(Maceracion, seguimiento_maceracion_coccion=SeguimientoMaceracionCoccion.objects.get(lote=Lote.objects.get(lote_nro=self.kwargs.get("pk"))), batch_nro=self.kwargs.get("batch"))

    def get_success_url(self):
        return reverse('maceracion_update',
                       kwargs={'pk': self.object.seguimiento_maceracion_coccion.lote.lote_nro, 'batch': self.object.batch_nro})

    def get_context_data(self, **kwargs):
        context = super(MaceracionUpdate, self).get_context_data(**kwargs)

        context['olla_maceracion_form_set'] = OllaMaceracionFormset(
            self.request.POST or None, instance=self.object)
        context['correccion_form_set'] = CorreccionFormset(
            self.request.POST or None, instance=self.object)
        context['olla_agua_caliente_form_set'] = OllaAguaCalienteFormset(
            self.request.POST or None, instance=self.object)
        context['pk'] = self.kwargs.get("pk")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        olla_maceracion_form_set = context['olla_maceracion_form_set']
        correccion_form_set = context['correccion_form_set']
        olla_agua_caliente_form_set = context['olla_agua_caliente_form_set']
        if form.is_valid():
            self.object = form.save()
            messages.success(self.request, 'Planilla Maceración guardada')
        if olla_maceracion_form_set.is_valid():
            olla_maceracion_form_set.instance = self.object
            olla_maceracion_form_set.save()
            messages.success(self.request, 'Datos Olla Maceración guardados')
        if correccion_form_set.is_valid():
            correccion_form_set.instance = self.object
            correccion_form_set.save()
            messages.success(self.request, 'Datos Corrección guardados')
        if olla_agua_caliente_form_set.is_valid():
            olla_agua_caliente_form_set.instance = self.object
            olla_agua_caliente_form_set.save()
            messages.success(
                self.request, 'Datos Olla Agua Caliente guardados')

        return super(MaceracionUpdate, self).form_valid(form)

    def form_invalid(self, form, correccion_form_set,
                     olla_maceracion_form_set,
                     olla_agua_caliente_form_set):
        messages.error(self.request, 'Error al guardar.')
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

    def get_success_url(self):
        return reverse('coccion_update',
                       kwargs={
                           'pk': self.object.proceso_maceracion_coccion.lote.lote_nro,
                           'batch': self.object.batch_nro})

    def form_valid(self, form):
        context = self.get_context_data()
        etapa_coccion_form_set = context['etapa_coccion_form_set']
        adicion_etapa_coccion_form_set = context['adicion_etapa_coccion_form_set']

        if form.is_valid():
            self.object = form.save()
            messages.success(self.request, 'Planilla Cocción guardada')
        print(etapa_coccion_form_set.errors)
        if etapa_coccion_form_set.is_valid():
            messages.success(self.request, 'Etapa Cocción gardada.')
            etapa_coccion_form_set.instance = self.object
            etapa_coccion_form_set.save()
        if adicion_etapa_coccion_form_set.is_valid():
            messages.success(self.request, 'Adición gardada.')
            adicion_etapa_coccion_form_set.instance = self.object
            adicion_etapa_coccion_form_set.save()
        return super(CoccionUpdate, self).form_valid(form)

    def form_invalid(self, form, etapa_coccion_form_set, adicion_etapa_coccion_form_set):
        messages.error(self.request, 'Error al guardar.')
        return self.render_to_response(self.get_context_data(form=form,
                                                             etapa_coccion_form_set=etapa_coccion_form_set,
                                                             adicion_etapa_coccion_form_set=adicion_etapa_coccion_form_set))

    def get_context_data(self, **kwargs):
        context = super(CoccionUpdate, self).get_context_data(**kwargs)
        context['etapa_coccion_form_set'] = EtapaCoccionFormset(
            self.request.POST or None, instance=self.object)
        context['adicion_etapa_coccion_form_set'] = AdicionEtapaCoccionFormset(
            self.request.POST or None, instance=self.object)
        context['pk'] = self.kwargs.get("pk")
        return context


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


@login_required
def SeguimientoFermentacionCreate(request, pk):
    """
    Inicializamos planilla de fermentación
    """
    init_planilla_Fermentacion(pk)
    return HttpResponseRedirect(reverse('lote_seguimientos_list',
                                        kwargs={'pk': pk}))
