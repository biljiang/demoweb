##
from django.urls import path
from . import views

app_name = 'shdky'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('v_tran_simu', views.VTrainSimuView.as_view(), name='VTrainSimu'),
    path('v_simu', views.VSimuView.as_view(), name='VSimu'),
    path('v_simu_table', views.v_simu_table, name='VSimuTable'),
    path('v_simu_upload_ajax', views.upload_ajax, name='VSimuFileupload'),
#    path('', views.index, name='index'),
]
