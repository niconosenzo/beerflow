from django import forms
from .models import Lote, SeguimientoMaceracionCoccion, Maceracion, Correccion, OllaMaceracion, OllaAguaCaliente, EtapaOllaAguaCaliente, Coccion, EtapaCoccion, Adicion, SeguimientoFermentacionClarificacion, SeguimientoCarbonatacion

    
class PlanillaMaceracionCoccion(forms.Form):

    # Seguimiento Maceracion Coccion
#    lote = forms.ModelChoiceField(queryset=Lote.objects.all(),disabled=True) # models.OneToOneField(Lote, on_delete=models.CASCADE, primary_key=True)
    lote = forms.IntegerField(disabled=True)
    fecha_inicio = forms.DateField(disabled=True) #models.DateField(help_text="Fecha inicio del proceso de coccion, campo requerido")
    fecha_fin = forms.DateField(required=False)   #models.DateField(null=True, blank=True)
    observaciones = forms.CharField(widget=forms.Textarea, required=False) #models.TextField(max_length=100, help_text="Comentarios,datos o informacion relevante para un lote determinado", null=True, blank=True)
    
    # Maceracion
    batch_nro = forms.IntegerField(disabled=True) #models.PositiveIntegerField(choices=NRO_BATCH, help_text="nro de batch correspondiente, puede ser 1 o 2")
    ## seguimiento_maceracion_coccion = forms.ModelChoiceField(disabled=True)#models.ForeignKey('SeguimientoMaceracionCoccion', on_delete=models.CASCADE, null=True)
    densidad_finalizacion_maceracion = forms.FloatField(required=False)#models.FloatField(null=True, blank=True)
    densidad_finalizacion_lavado = forms.FloatField(required=False) #models.FloatField(null=True, blank=True)
    observaciones = forms.CharField(widget=forms.Textarea, required=False) #models.TextField(max_length=100, help_text="Comentarios,datos o informacion relevante a la etapa de maceracion", null=True, blank=True)

    #Correccion(models.Model):
    ## maceracion = forms.ModelChoiceField(disabled=True) #models.ForeignKey('Maceracion', on_delete=models.CASCADE, null=True)
    inicial = forms.FloatField() #models.FloatField(null=True)
    acido_fosforico = forms.FloatField(required=False) #models.FloatField(null=True, blank=True)
    final_maceracion = forms.FloatField(help_text="Correción final del pH", required=False) #models.FloatField(null=True, blank=True)


    # OllaMaceracion:
    ## maceracion = forms.ModelChoiceField(disabled=True) #models.ForeignKey('Maceracion', on_delete=models.CASCADE, null=True)
    granos = forms.CharField(max_length=50) #models.CharField(max_length=50, help_text="Tipo de grano")
    cantidad = forms.FloatField(required=False) #models.FloatField(null=True, blank=True, help_text='Cantidad expresada en kilogramos')
    agua = forms.CharField(max_length=50,required=False, help_text="Litros") #models.CharField(max_length=50, help_text="Litros", null=True, blank=True)


    #OllaAguaCaliente(models.Model):
    ## maceracion = forms.ModelChoiceField(disabled=True)#models.ForeignKey('Maceracion', on_delete=models.CASCADE, null=True)
    agua_dureza = forms.CharField(max_length=50,empty_value=None, help_text="Dureza del agua dentro de la Olla Caliente",required=False) #models.CharField(max_length=50, help_text="dureza de agua dentro de Olla caliente", null=True, blank=True)
    agua_ph = forms.CharField(max_length=50, help_text="Dureza del agua dentro de la Olla Caliente",required=False) #models.CharField(max_length=50, help_text="ph del agua dentro Olla caliente", null=True, blank=True)
    filtracion_hora_inicio = forms.CharField(max_length=50, help_text="hora de inicio de filatracion") #models.CharField(max_length=50, help_text="hora inicio de filtracion")


    #EtapaOllaAguaCaliente(models.Model):
    ## olla_agua_caliente = forms.ModelChoiceField(disabled=True)#models.ForeignKey('OllaAguaCaliente', on_delete=models.CASCADE, null=True)
    NOMBRE_ETAPA = (
        ('empaste', 'Empaste'),
        ('maceracion', 'Maceracion'),
    )
    etapa_nombre = forms.CharField(max_length=50, widget=forms.Select(choices=NOMBRE_ETAPA))#models.CharField(max_length=50, choices=NOMBRE_ETAPA, help_text="etapa nombre, solo puede ser Empaste o Maceracion")
    etapa_hora_inicio = forms.CharField(max_length=50)#models.CharField(max_length=50, help_text="hora inicio")
    temperatura_R = forms.CharField(max_length=50,empty_value=None,required=False) #models.CharField(max_length=50, null=True, blank=True)
    temperatura_M = forms.CharField(max_length=50,empty_value=None,required=False) #models.CharField(max_length=50, null=True, blank=True)
    altura = forms.CharField(max_length=50,empty_value=None,required=False) #models.CharField(max_length=50, null=True, blank=True)
    agit_rec = forms.CharField(max_length=50,empty_value=None,required=False) #models.CharField(max_length=50, help_text="", null=True, blank=True)


