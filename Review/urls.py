from django.urls import path
from .views import (
    ReviewListView, write_review, FreelancerReviewListView,
    ReviewDetailView, ReviewUpdateView, ReviewDeleteView,
)

urlpatterns = [
    path('', ReviewListView.as_view(), name='review_list'),
    path('write/<int:contract_id>/', write_review, name='write_review'),
    path('write/<int:contract_id>/form/', write_review, name='review_form'),
    path('freelancer/<int:freelancer_id>/', FreelancerReviewListView.as_view(), name='freelancer_reviews'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
]
