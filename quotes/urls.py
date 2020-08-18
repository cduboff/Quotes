from django.urls import path
from . import views

urlpatterns = [
    path('', views.quotes),
    path('quotes/like/<int:id>', views.like),
    path('quotes/delete/<int:id>', views.delete),
]
