from django.urls import path

from . import views 

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/', views.admin_view, name='admin'),
    path('delete/<int:id>/', views.delete_product, name='delete'),
]