from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio_home, name='home'),
    path('personal/', views.personal_list, name='personal_list'),
    path('personal/<slug:slug>/', views.personal_detail, name='personal_detail'),
    path('company/', views.company_list, name='company_list'),
    path('company/<slug:slug>/', views.company_detail, name='company_detail'),
]
