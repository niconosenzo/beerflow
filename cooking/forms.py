from django import forms
from django.conf import settings
from django.forms import ModelForm, Textarea
import datetime
from django.contrib.admin import widgets
from django.forms.models import modelformset_factory, inlineformset_factory, BaseInlineFormSet
from .models import (
    Lote,
    SeguimientoMaceracionCoccion,
    Maceracion,
    Correccion,
    OllaMaceracion,
    OllaAguaCaliente,
    EtapaOllaAguaCaliente,
    Coccion,
    EtapaCoccion,
    SeguimientoFermentacion,
    SeguimientoCarbonatacion,
    SeguimientoClarificacionFiltracion,
    ParametrosFundamentales,
    InoculacionLevadura,
    RegistroFermentacion,
    AdicionCoccion,
    RegistroClarificacionFiltracion,
    Barril,
    MovimientosBarril
)


class SeguimientoMaceracionCoccionModelForm(forms.ModelForm):
    fecha_inicio = forms.DateField(disabled=True)
    fecha_inicio.widget.attrs.update({'autocomplete': 'off'})
    fecha_fin = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    fecha_fin.widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = SeguimientoMaceracionCoccion
        fields = ['fecha_inicio', 'fecha_fin', 'observaciones']

    def __init__(self, *args, **kwargs):
        super(SeguimientoMaceracionCoccionModelForm,
              self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            if field == 'observaciones':
                self.fields[field].widget.attrs.update({
                    'cols': 10,
                    'rows': 2
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
            if field == 'observaciones':
                self.fields[field].widget.attrs.update({
                    'cols': 10,
                    'rows': 2
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


class BarrilModelForm(forms.ModelForm):

    class Meta:
        model = Barril
        fields = ['barril_nro', 'observaciones']

    def __init__(self, *args, **kwargs):
        super(BarrilModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class MovimientosBarrilModelForm(forms.ModelForm):

    fecha = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    fecha.widget.attrs.update({'autocomplete': 'off'})
    ingresa = forms.DateField(
        required=False, input_formats=settings.DATE_INPUT_FORMATS)
    ingresa.widget.attrs.update({'autocomplete': 'off', 'required': 'False'})
    egresa = forms.DateField(
        required=False, input_formats=settings.DATE_INPUT_FORMATS)
    egresa.widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = MovimientosBarril
        fields = ['fecha', 'barril', 'lote', 'cliente', 'ingresa', 'egresa']

    def __init__(self, *args, **kwargs):
        super(MovimientosBarrilModelForm, self).__init__(*args, **kwargs)
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

############################
##########################
#########################


class OllaAguaCalienteModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OllaAguaCalienteModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = OllaAguaCaliente
        fields = ['agua_dureza', 'agua_ph', 'filtracion_hora_inicio']


class EtapaOllaAguaCalienteModelForm(forms.ModelForm):
    class Meta:
        model = EtapaOllaAguaCaliente
        fields = ['etapa_nombre', 'etapa_hora_inicio', 'temperatura_R',
                  'temperatura_M', 'altura', 'agit_rec']

    def __init__(self, *args, **kwargs):
        super(EtapaOllaAguaCalienteModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


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
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):

        result = super(BaseNestedFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


CorreccionFormset = inlineformset_factory(Maceracion, Correccion,
                                          form=CorreccionModelForm,
                                          fields=['inicial', 'acido_fosforico',
                                                  'final_maceracion'], extra=1,
                                          can_delete=False)

OllaMaceracionFormset = inlineformset_factory(Maceracion, OllaMaceracion,
                                              form=OllaMaceracionModelForm,
                                              fields=['granos', 'cantidad',
                                                      'agua'], extra=1,
                                              can_delete=False)


EtapaOllaAguaCalienteFormset = inlineformset_factory(OllaAguaCaliente,
                                                     EtapaOllaAguaCaliente,
                                                     form=EtapaOllaAguaCalienteModelForm,
                                                     fields=['etapa_nombre',
                                                             'etapa_hora_inicio',
                                                             'temperatura_R',
                                                             'temperatura_M',
                                                             'altura',
                                                             'agit_rec'],
                                                     extra=1,
                                                     can_delete=False)


OllaAguaCalienteFormset = inlineformset_factory(Maceracion,
                                                OllaAguaCaliente,
                                                form=OllaAguaCalienteModelForm,
                                                formset=BaseNestedFormset,
                                                fields=['agua_dureza', 'agua_ph', 'filtracion_hora_inicio'], extra=0,
                                                can_delete=False)


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
            if field == 'observaciones':
                self.fields[field].widget.attrs.update({
                    'cols': 10,
                    'rows': 2
                })


class EtapaCoccionModelForm(forms.ModelForm):
    etapa_nombre = forms.CharField(disabled=True)
    etapa_nombre.widget.attrs.update()

    class Meta:
        model = EtapaCoccion
        fields = ['etapa_nombre', 'etapa_hora_inicio']

    def __init__(self, *args, **kwargs):
        super(EtapaCoccionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


EtapaCoccionFormset = inlineformset_factory(Coccion, EtapaCoccion,
                                            form=EtapaCoccionModelForm,
                                            extra=0,
                                            can_delete=False)


class AdicionEtapaCoccionModelForm(forms.ModelForm):

    class Meta:
        model = AdicionCoccion
        fields = ['tipo', 'gramos', 'hora_adicion']

    def __init__(self, *args, **kwargs):
        super(AdicionEtapaCoccionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


AdicionEtapaCoccionFormset = inlineformset_factory(Coccion, AdicionCoccion,
                                                   form=AdicionEtapaCoccionModelForm,
                                                   extra=1,
                                                   can_delete=False)

# SeguimientoCarbonatacion,
# SeguimientoClarificacionFiltracion
# RegistroClarificacionFiltracion

# PLANILLA FERMENTACION


class SeguimientoFermentacionModelForm(forms.ModelForm):
    # fecha_llenado = forms.DateField(widget=forms.SelectDateWidget())
    fecha_llenado = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    fecha_llenado.widget.attrs.update({'autocomplete': 'off'})
    fecha_inoculacion_levadura = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS)
    fecha_inoculacion_levadura.widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = SeguimientoFermentacion
        fields = ['vasija', 'fecha_llenado', 'litros',
                  'fecha_inoculacion_levadura', 'tipo_levadura']

    def __init__(self, *args, **kwargs):
        super(SeguimientoFermentacionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class RegistroFermentacionModelForm(forms.ModelForm):

    fecha = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    fecha.widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = RegistroFermentacion
        fields = ['fecha', 'hora',
                  'densidad', 'temp_sala', 'temp_mosto', 'pH', 'observaciones']

    def __init__(self, *args, **kwargs):
        super(RegistroFermentacionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            if field == 'observaciones':
                self.fields[field].widget.attrs.update({
                    'cols': 10,
                    'rows': 2
                })


class InoculacionLevaduraModelForm(forms.ModelForm):
    class Meta:
        model = InoculacionLevadura
        fields = ['hora', 'levadura', 'dosis', 'temp_sala', 'temp_mosto',
                  'densidad', 'observaciones']

    def __init__(self, *args, **kwargs):
        super(InoculacionLevaduraModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            if field == 'observaciones':
                self.fields[field].widget.attrs.update({
                    'cols': 10,
                    'rows': 2
                })


class ParametrosFundamentalesModelForm(forms.ModelForm):
    class Meta:
        model = ParametrosFundamentales
        fields = ['dO', 'dF', 'alcohol_teorico', 'pH_inicial',
                  'pH_final', 'observaciones']

    def __init__(self, *args, **kwargs):
        super(ParametrosFundamentalesModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            if field == 'observaciones':
                self.fields[field].widget.attrs.update({
                    'cols': 10,
                    'rows': 2
                })


RegistroFermentacionFormset = inlineformset_factory(SeguimientoFermentacion, RegistroFermentacion,
                                                    form=RegistroFermentacionModelForm,
                                                    fields=['fecha', 'hora', 'densidad',
                                                            'temp_sala', 'temp_mosto',
                                                            'pH', 'observaciones'],
                                                    extra=1,
                                                    can_delete=False)
