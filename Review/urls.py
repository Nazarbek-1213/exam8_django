from django.urls import path
from .views import *

urlpatterns = [
    path('', ReviewListView.as_view(), name='review_list'),
    path('create/',write_review, name='write'),
    path('freelancer/<int:freelancer_id>/', FreelancerReviewListView.as_view(), name='write_review'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
]