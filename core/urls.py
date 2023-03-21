from django.urls import path

from . import views 

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/', views.admin_view, name='admin'),
    path('delete/<int:id>/', views.delete_product, name='delete'),
    path('create-product/', views.create_product, name='create-product'),
    path('update-product/<int:id>/', views.update_product, name='update-product'),
    path('users/', views.view_users, name='users'),
]