from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
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


class maceracionCoccionUpdate(LoginRequiredMixin,UpdateView):
    model = SeguimientoMaceracionCoccion
    template_name = 'planilla_maceracion_coccion.html'
    form_class = SeguimientoMaceracionCoccionModelForm

    def get_success_url(self):
        return reverse_lazy('maceracion_coccion_update',
                       kwargs={'pk': self.object.lote.lote_nro})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # Planilla Maceracion
        maceraciones = Maceracion.objects.filter(seguimiento_maceracion_coccion=self.object).order_by('pk')
        maceracion_data = []
        correccion_data = []
    
        for maceracion in maceraciones:
            print(maceracion)
            d = {'batch_nro': maceracion.batch_nro,
                  'densidad_finalizacion_maceracion': maceracion.densidad_finalizacion_maceracion,
                  'densidad_finalizacion_lavado': maceracion.densidad_finalizacion_lavado,
                  'observaciones': maceracion.observaciones}
            maceracion_data.append(d)
        #     ## por cada maceracion, buscamos los objetos Correccion pH
        #
        #     correcciones = Correccion.objects.filter(maceracion=maceracion)
        #     for correccion in correcciones:
        #         print(correccion)
        #         d1 = {'inicial': correccion.inicial,
        #               'acido_fosforico': correccion.acido_fosforico,
        #               'final_maceracion': correccion.final_maceracion}
        #         correccion_data.append(d1)
        #     correccion_form_set = CorreccionFormSet(initial=correccion_data)
        # #print(correccion_data)
        maceracion_form_set = MaceracionSeguimientosFormSet(initial=maceracion_data)
        correccion_form_set = CorreccionFormSet(initial=correccion_data)


        #
        # Planilla Coccion
        cocciones = Coccion.objects.filter(proceso_maceracion_coccion=self.object).order_by('pk')
        coccion_data = []
        for coccion in cocciones:
            d = {'batch_nro': coccion.batch_nro,
                  'densidad_finalizacion_hervor': coccion.densidad_finalizacion_hervor,
                  'hora_fin_trasiego': coccion.hora_fin_trasiego,
                  'observaciones': coccion.observaciones}
            coccion_data.append(d)
            ##
        coccion_form_set = CoccionSeguimientosFormSet(initial=coccion_data)
        #

        return self.render_to_response(self.get_context_data(form=form,
                                                             maceracion_form_set=maceracion_form_set,
                                                             coccion_form_set=coccion_form_set,
                                                             correccion_form_set=correccion_form_set))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        maceracion_form_set = MaceracionSeguimientosFormSet(request.POST)
        coccion_form_set = CoccionSeguimientosFormSet(request.POST)
        correccion_form_set = CorreccionFormSet(request.POST)
        if form.is_valid() and maceracion_form_set.is_valid() and coccion_form_set.is_valid() and correccion_form_set.is_valid():
            return self.form_valid(form, maceracion_form_set,
                                   coccion_form_set, correccion_form_set)
        else:
            return self.form_invalid(form, maceracion_form_set,
                                     coccion_form_set, correccion_form_set)

    def form_valid(self, form, maceracion_form_set, coccion_form_set, correccion_form_set):
        self.object = form.save()
        #Maceracion
        # maceracion_form_set.instance = self.object
        # ##Maceracion-Correccion
        # #correccion_form_set.instance = maceracion_form_set.instance
        # #Correccion.objects.filter(maceracion=Maceracion.objects.filter(seguimiento_maceracion_coccion=self.object.pk)).delete()
        # #Maceracion.objects.filter(seguimiento_maceracion_coccion=self.object.pk).delete()
        # maceracion_form_set.save()
        # correccion_form_set.save()

        #Coccion
        coccion_form_set.instance = self.object
        Coccion.objects.filter(proceso_maceracion_coccion=self.object.pk).delete()
        coccion_form_set.save()


        # return HttpResponseRedirect(self.success_url)
        return self.render_to_response(self.get_context_data(form=form,
                                                             maceracion_form_set=maceracion_form_set,
                                                             coccion_form_set=coccion_form_set,
                                                             correccion_form_set=correccion_form_set))

    def form_invalid(self, form, maceracion_form_set, coccion_form_set):
        return self.render_to_response(self.get_context_data(form=form,
                                                             maceracion_form_set=maceracion_form_set,
                                                             coccion_form_set=occion_form_set,
                                                             correccion_form_set=correccion_form_set))


# def maceracionCoccionUpdate(request, pk, batch):
#
#     # """
#     # formulario Planilla Maceracion, se incluyen los formularios de Correccion,
#     # Olla maceracion, Olla agua caliente y sus etapas.
#     # """
#     # obj_maceracion = get_object_or_404(Maceracion,
#     #                         seguimiento_maceracion_coccion=pk, batch_nro=batch)
#     # obj_correccion = get_object_or_404(Correccion, maceracion = obj_maceracion)
#     #
#     # form_maceracion = MaceracionModelForm(request.POST or None,
#     #                                       instance=obj_maceracion)
#     # form_correccion = CorreccionModelForm(request.POST or None,
#     #                                       instance=obj_correccion)
#     #
#     # template_name = 'cooking/planillaMaceracion.html'
#     # context = {'form_maceracion': form_maceracion,
#     #            'obj_maceracion': obj_maceracion,
#     #            'form_correccion': form_correccion,
#     #            }
#     # # si es POST, agregamos la nota
#     # if request.method == 'POST':
#     #     filledform_maceracion = MaceracionModelForm(request.POST)
#     #     filledform_correccion = CorreccionModelForm(request.POST)
#     #
#     #     if form_maceracion.is_valid() and form_correccion.is_valid():
#     #         note = '-- Planilla Actualizada %s --' %(time.strftime("%Y-%m-%d %H:%M"))
#     #         form_maceracion.save()
#     #         form_correccion.save()
#     #     else:
#     #         note = 'No se pudo guardar la planilla'
#     #     context['note'] = note
#     #     context['form_maceracion'] = filledform_maceracion
#     #     context['form_correccion'] = filledform_correccion
#     #
#     # return render(request, template_name, context)


def coccionUpdate(request, pk, batch):
    #    obj = get_object_or_404(BlogPost, slug=slug)
    #    form = BlogPostModelForm(request.POST or None, instance=obj)
    #    if form.is_valid():
    #        form.save()
    #    template_name = 'form.html'
    #    context = {'form': form, "title": f"Update {obj.title}"}
    #    return render(request, template_name, context)
    pass


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
