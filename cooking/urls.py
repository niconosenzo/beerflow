from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lote/$', views.LoteView.as_view(), name='lotelist'),
    url(r'^lote/(?P<pk>\d+)$', views.LoteSeguimientosView.as_view(),
        name='lote_seguimientos_list'),
]

urlpatterns += [
    url(r'^lote/create/$', views.LoteCreate.as_view(), name='lote_create'),
    url(r'^lote/(?P<pk>\d+)/BatchMaceracionCoccion/$',
        views.BatchMaceracionCoccionlist.as_view(),
        name='batch_maceracion_coccion_list'),
    # url(r'^lote/(?P<pk>\d+)/(?P<batch>\d+)/updateMaceracionCoccion/$',
    #     views.maceracionCoccionUpdate.as_view(), name='maceracion_coccion_update'),
    url(r'^lote/(?P<pk>\d+)/updateMaceracionCoccion/$',
        views.maceracionCoccionUpdate.as_view(), name='maceracion_coccion_update'),
    url(r'^lote/(?P<pk>\d+)/(?P<batch>\d+)/updateCoccion/$',
        views.coccionUpdate, name='coccion_update'),
    url(r'^lote/(?P<pk>\d+)/createMaceracionCoccion/$',
        views.SeguimientoMaceracionCoccionCreate,
        name='maceracion_coccion_create'),
]
