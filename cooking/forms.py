from django import forms
    
class PlanillaMaceracionCoccion(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    lote = models.OneToOneField(Lote, on_delete=models.CASCADE, primary_key=True)
    fecha_inicio = models.DateField(help_text="Fecha inicio del proceso de coccion, campo requerido")
    fecha_fin = models.DateField(null=True, blank=True)
    observaciones = models.TextField(max_length=100, help_text="Comentarios,datos o informacion relevante para un lote determinado", null=True, blank=True)
    
