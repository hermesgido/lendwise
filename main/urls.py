from django.urls import path
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('clients/', views.clients, name='clients'),
    path('add_client/', views.add_client, name='add_client'),
    path('loans/', views.loans, name='loans'),
    path('add_loan/', views.add_loan, name='add_loan'),
    path('view_loan/<str:id>/', views.view_loan, name="view_loan"),
    


]
