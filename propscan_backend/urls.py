"""propscan_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views


# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# from .views import TokenObtainView, token_verify_view

urlpatterns = [
    # path('api/token/', TokenObtainView.as_view(), name='token_obtain'),
     path('api/token/', views.generate_jwt_token, name='token_obtain'),
       path('api/token/verify/', views.verify_jwt_token, name='verify_jwt_token'),
    # path('api/token/verify/', token_verify_view, name='token_verify'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #  path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api-auth/', include('rest_framework.urls')),
    path('',views.homepage),
    path('admin/', admin.site.urls),
    # path('login/',views.login,name="login"),
    # path('register_broker/',views.register_broker,name="register_broker"),
    # path('register_user/',views.register_user,name='register_user'),
    path('wallet/', include('wallet.urls')),
    path('property/',include('property_listing.urls')),
    path("", include("chat.urls")),
    path("",include("property_listing.urls")),
    path("",include("kyc.urls")),

    path("accounts/", include("accounts.urls")),
    path("firebase-messaging-sw.js",views.showFirebaseJS,name="showFirebaseJS"),
    path("send-notif/",views.send_notification,name="send-notif")
  
  


    




]
