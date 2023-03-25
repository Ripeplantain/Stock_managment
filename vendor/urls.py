from django.urls import path
from . import views


urlpatterns = [
    path('vendor-form/', views.vendor_form, name='vendor-form'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor-dashboard'),
]