from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),

    path('profile/', ProfileView, name='profile'),
    path('edit-profile/', EditProfile, name='edit_profile'),

    path('search/', SearchView, name='search'),

    path('main-redirect/', main_redirect, name='main-redirect'),

    path('main-client/live-projects/', liveProView, name='live_projects'),
    path('main-client/avg-rating/', AvgRateView, name='avg_rating'),
    path('main-client/finished-work/', FinishedWorkView, name='finished_work'),
    path('main-client/freelancer-count/', FreelancerView, name='freelancer_count'),
    path('main-client/', liveProView, name='main_client'),


    path('main-freelancer/all-projects/', AllProview, name='main_freelancer'),
    path('logo/', logo_redirect, name='logo_redirect'),
    path('all-projects/', AllProview, name='all_freelancer'),
path('profile/<int:pk>/', UserProfileView, name='user_profile')
]