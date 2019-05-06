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
    url(r'^lote/(?P<pk>\d+)/updateMaceracionCoccion/$', views.SeguimientoMaceracionCoccionUpdate, name='maceracion_coccion_update'),
    url(r'^lote/(?P<pk>\d+)/createMaceracionCoccion/$', views.SeguimientoMaceracionCoccionCreate, name='maceracion_coccion_create'),
]

#urlpatterns += [   
#    url(r'^lote/(?P<pk>[-\w]+)/createMaceracionCoccion/$', views.SeguimientoMaceracionCoccionCreate, name='maceracion_coccion_create'),
#]

#urlpatterns += [
#    url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
#]
