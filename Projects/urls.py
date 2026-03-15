from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateProView, name='create_post'),
    path('myprojects/', views.SelfProjectsView, name='myprojects'),
    path('project/<int:id>/', views.ProjectdetailsView, name='project_detail'),
    path('project/<int:id>/delete/', views.DeleteProjectView, name='project_delete'),
    path('project/<int:id>/edit/', views.EditProjectView, name='edit_project'),
]