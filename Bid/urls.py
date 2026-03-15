from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('project/<int:pk>/bid/', views.place_bid, name='place_bid'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),

    path('bid/<int:bid_id>/accept/', accept_bid, name='accept_bid'),
    path('bid/<int:bid_id>/reject/', reject_bid, name='reject_bid'),
]