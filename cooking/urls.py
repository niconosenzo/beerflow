from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.LoteView.as_view(), name='lotelist'),
    url(r'^lote/$', views.LoteView.as_view(), name='lotelist'),
    url(r'^lote/(?P<pk>\d+)$', views.LoteSeguimientosView.as_view(),
        name='lote_seguimientos_list'),
]

urlpatterns += [
    url(r'^lote/create/$', views.LoteCreate.as_view(), name='lote_create'),
    url(r'^lote/(?P<pk>\d+)/BatchMaceracionCoccion/$',
        views.BatchMaceracionCoccionlist.as_view(),
        name='batch_maceracion_coccion_list'),
    url(r'^lote/(?P<pk>\d+)/Fermentacion/$',
        views.FermentacionUpdate.as_view(),
        name='fermentacion_list'),
    url(r'^lote/(?P<pk>\d+)/(?P<batch>\d+)/updateMaceracion/$',
        views.MaceracionUpdate.as_view(), name='maceracion_update'),
    url(r'^lote/(?P<pk>\d+)/(?P<batch>\d+)/updateCoccion/$',
        views.CoccionUpdate.as_view(), name='coccion_update'),
    url(r'^lote/(?P<pk>\d+)/createMaceracionCoccion/$',
        views.SeguimientoMaceracionCoccionCreate,
        name='maceracion_coccion_create'),
    url(r'^lote/(?P<pk>\d+)/createFermentacion/$',
        views.SeguimientoFermentacionCreate,
        name='fermentacion_create'),
]
