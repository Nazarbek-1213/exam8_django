from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:project_id>/<int:freelancer_id>/', views.create_contract, name='create_contract'),
    path('detail/<int:contract_id>/', views.contract_detail, name='contract_detail'),

    path('client/list/', views.client_contract_list, name='client_contract_list'),
    path('freelancer/list/', views.freelancer_contract_list, name='freelancer_contract_list'),
    path('all/', views.all_contracts, name='all_contracts'),

    path('active/', views.active_contracts, name='active_contracts'),
    path('finished/', views.finished_contracts, name='finished_contracts'),
    path('cancelled/', views.cancelled_contracts, name='cancelled_contracts'),

    path('finish/<int:contract_id>/', views.finish_contract, name='finish_contract'),
    path('cancel/<int:contract_id>/', views.cancel_contract, name='cancel_contract'),


]