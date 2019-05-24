from django import forms
from .models import Lote, SeguimientoMaceracionCoccion, Maceracion, Correccion, OllaMaceracion, OllaAguaCaliente, EtapaOllaAguaCaliente, Coccion, EtapaCoccion, Adicion, SeguimientoFermentacionClarificacion, SeguimientoCarbonatacion
from django.forms.models import modelformset_factory, inlineformset_factory, BaseInlineFormSet
from .utils.forms import is_empty_form, is_form_persisted
from .custom_layout_object import *




class SeguimientoMaceracionCoccionModelForm(forms.ModelForm):
    fecha_inicio = forms.DateField(disabled=True)
    fecha_fin = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = SeguimientoMaceracionCoccion
        fields = ['fecha_inicio', 'fecha_fin', 'observaciones']

    def __init__(self, *args, **kwargs):
        super(SeguimientoMaceracionCoccionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })




class MaceracionModelForm(forms.ModelForm):
    batch_nro = forms.CharField(disabled=True)
    batch_nro.widget.attrs.update({'size': 1, 'title': 'Batch número:'})


    class Meta:
        model = Maceracion
        fields = ['batch_nro', 'densidad_finalizacion_maceracion',
                  'densidad_finalizacion_lavado', 'observaciones']

    def __init__(self, *args, **kwargs):
        super(MaceracionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class LoteModelForm(forms.ModelForm):


    class Meta:
        model = Lote
        fields = ['lote_nro', 'observaciones']

    def __init__(self, *args, **kwargs):
        super(LoteModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })



class CoccionModelForm(forms.ModelForm):
    batch_nro = forms.CharField(max_length=1, disabled=True)
    batch_nro.widget.attrs.update({'size': 1, 'title': 'Batch número:'})

    class Meta:
        model = Coccion
        fields = ['batch_nro', 'densidad_finalizacion_hervor',
                  'hora_fin_trasiego', 'observaciones']

    def __init__(self, *args, **kwargs):
        super(CoccionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class CorreccionModelForm(forms.ModelForm):
    class Meta:
        model = Correccion
        fields = ['inicial', 'acido_fosforico', 'final_maceracion']

    def __init__(self, *args, **kwargs):
        super(CorreccionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class OllaMaceracionModelForm(forms.ModelForm):
    class Meta:
        model = OllaMaceracion
        fields = ['granos', 'cantidad', 'agua']

    def __init__(self, *args, **kwargs):
        super(OllaMaceracionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class OllaAguaCalienteModelForm(forms.ModelForm):
    class Meta:
        model = OllaAguaCaliente
        fields = ['agua_dureza', 'agua_ph', 'filtracion_hora_inicio']


class EtapaOllaAguaCalienteModelForm(forms.ModelForm):
    class Meta:
        model = EtapaOllaAguaCaliente
        fields = ['etapa_nombre', 'etapa_hora_inicio', 'temperatura_R',
                  'temperatura_M', 'altura', 'agit_rec']




class BaseNestedFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseNestedFormset, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = EtapaOllaAguaCalienteFormset(
            instance=form.instance,
            data=form.data if self.is_bound else None,
            prefix='%s-%s' % (
                form.prefix,
                EtapaOllaAguaCalienteFormset.get_default_prefix(),
            ),
        )


    def is_valid(self):
        result = super(BaseNestedFormset, self).is_valid()

        if self.is_bound:
            # look at any nested formsets, as well
            for form in self.forms:
                if hasattr(form, 'nested'):
                    print("tiene nested")
                    result = result and form.nested.is_valid()
                    print(form.nested.is_valid())
        return result


    def save(self, commit=True):

        result = super(BaseNestedFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result
    # 
    # def clean(self):
    #     """
    #     If a parent form has no data, but its nested forms do, we should
    #     return an error
    #     """
    #     super().clean()
    #
    #     for form in self.forms:
    #         if not hasattr(form, 'nested') or self._should_delete_form(form):
    #             continue
    #
    #         if self._is_adding_nested_inlines_to_empty_form(form):
    #             form.add_error(
    #                 field=None,
    #                 error=_('Estás intentando agregar etapas a un Olla de Agua '
    #                         'caliente que aún no existe'))
    #
    # def _is_adding_nested_inlines_to_empty_form(self, form):
    #     """
    #     Are we trying to add data in nested inlines to a form that has no data?
    #     e.g. Adding Images to a new Book whose data we haven't entered?
    #     """
    #     if not hasattr(form, 'nested'):
    #         # A basic form; it has no nested forms to check.
    #         return False
    #
    #     if is_form_persisted(form):
    #         # We're editing (not adding) an existing model.
    #         return False
    #
    #     if not is_empty_form(form):
    #         # The form has errors, or it contains valid data.
    #         return False
    #
    #     # All the inline forms that aren't being deleted:
    #     non_deleted_forms = set(form.nested.forms).difference(
    #         set(form.nested.deleted_forms)
    #     )
    #
    #
    #     # At this point we know that the "form" is empty.
    #     # In all the inline forms that aren't being deleted, are there any that
    #     # contain data? Return True if so.
    #     return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


CorreccionFormset = inlineformset_factory(Maceracion, Correccion,
                                          fields=['inicial', 'acido_fosforico',
                                                  'final_maceracion'], extra=1,
                                          can_delete=True)

OllaMaceracionFormset = inlineformset_factory(Maceracion, OllaMaceracion,
                                              fields=['granos','cantidad',
                                                        'agua'], extra=1,
                                              can_delete=True)


EtapaOllaAguaCalienteFormset = inlineformset_factory(OllaAguaCaliente, EtapaOllaAguaCaliente,
                                          fields=['etapa_nombre', 'etapa_hora_inicio', 'temperatura_R',
                                                    'temperatura_M', 'altura', 'agit_rec'], extra=1,
                                          can_delete=True)

OllaAguaCalienteFormset = inlineformset_factory(Maceracion,
                                                      OllaAguaCaliente,
                                                      formset=BaseNestedFormset,
                                                      fields= ['agua_dureza', 'agua_ph', 'filtracion_hora_inicio'],extra=0,
                                                      can_delete=False)
