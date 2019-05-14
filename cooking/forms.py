from django import forms
from .models import Lote, SeguimientoMaceracionCoccion, Maceracion, Correccion, OllaMaceracion, OllaAguaCaliente, EtapaOllaAguaCaliente, Coccion, EtapaCoccion, Adicion, SeguimientoFermentacionClarificacion, SeguimientoCarbonatacion
from django.forms.models import modelformset_factory, inlineformset_factory


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
    # batch_nro = forms.CharField(max_length=1, disabled=True)
    # batch_nro.widget.attrs.update({'size': 1, 'title': 'Batch número:'})

    class Meta:
        model = Maceracion
        fields = ['batch_nro','densidad_finalizacion_maceracion',
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

# extra=2 ya que sólo pueden haber 2 batches tanto para cocción como para maceración
MaceracionSeguimientosFormSet = inlineformset_factory(SeguimientoMaceracionCoccion, Maceracion, form=MaceracionModelForm, extra=2)
CoccionSeguimientosFormSet = inlineformset_factory(SeguimientoMaceracionCoccion, Coccion, form=CoccionModelForm, extra=2)
CorreccionFormSet = inlineformset_factory(Maceracion, Correccion, form=CorreccionModelForm, extra=4)
