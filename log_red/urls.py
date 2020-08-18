from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('edit_user/<int:id>', views.edit_user),
    path('user/<int:id>', views.user),
    path('back', views.back),
]
