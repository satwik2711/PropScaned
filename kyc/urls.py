from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("aadharkyc/", views.aadharkyc, name="aadharkyc"),
    # path("auth_token/", views.auth_token, name="auth_token"),
]