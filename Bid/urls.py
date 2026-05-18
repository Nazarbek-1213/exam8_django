from django.urls import path
from . import views

urlpatterns = [
    path('project/<int:pk>/bid/', views.place_bid, name='place_bid'),
    path('my-bids/', views.my_bids, name='my_bids'),

    path('bid/<int:bid_id>/accept/', views.accept_bid, name='accept_bid'),
    path('bid/<int:bid_id>/reject/', views.reject_bid, name='reject_bid'),
]
