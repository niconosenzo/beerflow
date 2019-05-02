from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lote/$', views.LoteView.as_view(), name='lotelist'),
    #    path('lote/', views.LoteView.as_view(), name='lotelist'),
    #    path('<int:pk>/', views.LoteSeguimientosView.as_view(), name='lote_seguimientos_list'),
    url(r'^lote/(?P<pk>\d+)$', views.LoteSeguimientosView.as_view(), name='lote_seguimientos_list'),
]

