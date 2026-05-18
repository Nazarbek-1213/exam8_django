from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('conv/<int:conv_id>/', views.conversation_detail, name='conversation'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('start/<int:user_id>/project/<int:project_id>/', views.start_conversation, name='start_conversation_project'),
]
