from django.urls import path
from .views import (
    LoginView, RegisterView, LogoutView,
    ProfileView, EditProfile, SearchView,
    main_redirect, liveProView, AllProview,
    logo_redirect, UserProfileView,
)

urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),

    path('profile/', ProfileView, name='profile'),
    path('edit-profile/', EditProfile, name='edit_profile'),

    path('search/', SearchView, name='search'),

    path('main-redirect/', main_redirect, name='main-redirect'),
    path('home/', main_redirect, name='main'),
    path('start/', main_redirect, name='home'),

    path('main-client/', liveProView, name='main_client'),

    path('main-freelancer/all-projects/', AllProview, name='main_freelancer'),
    path('logo/', logo_redirect, name='logo_redirect'),
    path('all-projects/', AllProview, name='all_freelancer'),
    path('profile/<int:pk>/', UserProfileView, name='user_profile'),
]
