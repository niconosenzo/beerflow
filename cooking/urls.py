from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('lote/', views.LoteView.as_view(), name='lotelist'),
]

