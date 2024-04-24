from django.urls import path
from . import views
from .views import BlockUserView, DeleteConversationView

urlpatterns = [
    path('<str:room_name>/', views.room, name='room'),
     path('block_user/<str:room_name>/', BlockUserView.as_view(), name='block_user'),
    path('delete_conversation/<str:room_name>/', DeleteConversationView.as_view(), name='delete_conversation'),
]