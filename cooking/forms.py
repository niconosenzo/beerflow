from django import forms
from .models import Lote, SeguimientoMaceracionCoccion, Maceracion, Correccion, OllaMaceracion, OllaAguaCaliente, EtapaOllaAguaCaliente, Coccion, EtapaCoccion, Adicion, SeguimientoFermentacionClarificacion, SeguimientoCarbonatacion
from django.forms.models import modelformset_factory, inlineformset_factory, BaseInlineFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *




class SeguimientoMaceracionCoccionModelForm(forms.ModelForm):
    fecha_inicio = forms.DateField(disabled=True)
    fecha_fin = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = SeguimientoMaceracionCoccion
        fields = ['fecha_inicio', 'fecha_fin', 'observaciones']


    def __init__(self, *args, **kwargs):
        super(SeguimientoMaceracionCoccionModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('fecha_inicio'),
                Field('fecha_fin'),
                Field('observaciones'),
                Fieldset('Maceracion',
                     Formset('maceraciones')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
                )
            )

class MaceracionModelForm(forms.ModelForm):
    batch_nro = forms.CharField(disabled=True)
    # batch_nro.widget.attrs.update({'size': 1, 'title': 'Batch número:'})


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


class CoccionModelForm(forms.ModelForm):
    # batch_nro = forms.CharField(max_length=1, disabled=True)
    # batch_nro.widget.attrs.update({'size': 1, 'title': 'Batch número:'})

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


class OllaAguaCalienteModelForm(forms.ModelForm):
    class Meta:
        model = OllaAguaCaliente
        fields = ['agua_dureza', 'agua_ph', 'filtracion_hora_inicio']


class EtapaOllaAguaCalienteModelForm(forms.ModelForm):
    class Meta:
        model = EtapaOllaAguaCaliente
        fields = ['etapa_nombre', 'etapa_hora_inicio', 'temperatura_R',
                  'temperatura_M', 'altura', 'agit_rec']


CorreccionFormset = inlineformset_factory(Maceracion, Correccion,
                                          fields=['inicial', 'acido_fosforico',
                                                  'final_maceracion'], extra=2,
                                          can_delete=True)


class BaseNestedFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseNestedFormset, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = CorreccionFormset(
            instance=form.instance,
            data=form.data if self.is_bound else None,
            prefix='%s-%s' % (
                form.prefix,
                CorreccionFormset.get_default_prefix(),
            ),
        )

    def is_valid(self):

        result = super(BaseNestedFormset, self).is_valid()

        if self.is_bound:
            # look at any nested formsets, as well
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()
        return result

    def save(self, commit=True):

        result = super(BaseNestedFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result



# extra=2 ya que sólo pueden haber 2 batches tanto para cocción como para maceración
MaceracionCoccionFormSet = inlineformset_factory(SeguimientoMaceracionCoccion,
                                                      Maceracion,
                                                      formset=BaseNestedFormset,
                                                      fields= ['batch_nro', 'densidad_finalizacion_maceracion',
                                                                'densidad_finalizacion_lavado', 'observaciones'],extra=0)
# CoccionSeguimientosFormSet = inlineformset_factory(SeguimientoMaceracionCoccion,
#                                                    Coccion,
#                                                    form=CoccionModelForm,
#                                                    extra=2)
