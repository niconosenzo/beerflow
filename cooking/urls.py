from django.conf.urls import url
from . import views


# URLs barril | lote | movimientos
urlpatterns = [
    # Create object URLs
    url(r'^lote/create/$', views.LoteCreate.as_view(), name='lote_create'),
    url(r'^barril/create/$', views.BarrilCreate.as_view(),
        name='barril_create'),
    url(r'^movimiento/create/$', views.MovimientosBarrilCreate.as_view(),
        name='movimiento_create'),
    url(r'^$', views.LoteView.as_view(), name='lotelist'),
    url(r'^lote/$', views.LoteView.as_view(), name='lotelist'),
    url(r'^barril/$', views.BarrilView.as_view(), name='barrillist'),
    url(r'^movimiento/$', views.MovimientosBarrilView.as_view(),
        name='movimientoslist'),
    url(r'^movimiento/(?P<lote>\d+)',
        views.LoteMovimientosBarrilView.as_view(),
        name='movimientoslistlote'),
    url(r'^movimiento/(?P<barril>[-\w]+)/$',
        views.BarrilMovimientosBarrilView.as_view(),
        name='movimientoslistbarril'),
    url(r'^lote/(?P<pk>\d+)$', views.LoteSeguimientosView.as_view(),
        name='lote_seguimientos_list'),
    url(r'^movimiento/update/(?P<pk>\d+)/$',
        views.UpdateMovimientosBarrilView.as_view(),
        name='movimientosupdate'),
    url(r'^movimiento/ingresarbarril/(?P<slug>[-\w]+)/$',
        views.IngresarMovimientosBarrilView.as_view(),
        name='movimientosingreso'),
]

# URLs planillas

urlpatterns += [
    # Planillas
    url(r'^lote/(?P<pk>\d+)/BatchMaceracionCoccion/$',
        views.BatchMaceracionCoccionlist.as_view(),
        name='batch_maceracion_coccion_list'),
    url(r'^lote/(?P<pk>\d+)/Fermentacion/$',
        views.FermentacionUpdate.as_view(),
        name='fermentacion_list'),
    url(r'^lote/(?P<pk>\d+)/ClarificacionFiltracion/$',
        views.ClarificacionFiltracionUpdate.as_view(),
        name='clarificacion_filtracion_list'),
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
    url(r'^lote/(?P<pk>\d+)/createClarificacionFiltracion/$',
        views.SeguimientoClarificacionFiltracionCreate,
        name='clarificacion_filtracion_create'),
]
