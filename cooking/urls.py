from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lote/$', views.LoteView.as_view(), name='lotelist'),
    url(r'^lote/(?P<pk>\d+)$', views.LoteSeguimientosView.as_view(), name='lote_seguimientos_list'),
]
urlpatterns += [  
    url(r'^lote/create/$', views.LoteCreate.as_view(), name='lote_create'),
    #    url(r'^lote/(?P<pk>\d+)/update/$', views.LoteUpdate.as_view(), name='lote_update'),
    #    url(r'^lote/(?P<pk>\d+)/delete/$', views.LoteDelete.as_view(), name='lote_delete'),
]
