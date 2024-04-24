from django.urls import path
from . import views


urlpatterns = [
    path('register', views.signup),
    path('login_user/', views.login_user),
    path('buyers/', views.get_buyer),
    path('owners/', views.get_owner),
    path('brokers/', views.get_broker),
    path('delete/<int:pk>/', views.delete),
    path('update/buyer/<int:pk>/', views.update_buyer),
    path('update/owner/<int:pk>/', views.update_owner),
    path('update/broker/<int:pk>/', views.update_broker),
    path('nearby_experts/', views.nearby_experts),
    path('favorites/type1/<int:user_id>/<int:property_id>/', views.add_favorite_type1, name='add-favorite-type1'),
    path('favorites/type2/<int:user_id>/<int:property_id>/', views.add_favorite_type2, name='add-favorite-type2'),
    path('favorites/type3/<int:user_id>/<int:property_id>/', views.add_favorite_type3, name='add-favorite-type3')

]