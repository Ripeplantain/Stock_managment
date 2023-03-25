from django.urls import path

from . import views 

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('admin/', views.admin_view, name='admin'),
    path('delete/<int:id>/', views.delete_product, name='delete'),
    path('create-product/', views.create_product, name='create-product'),
    path('update-product/<int:id>/', views.update_product, name='update-product'),
    # path('users/', views.view_users, name='users'),
    path('orders/<int:id>/', views.order_view, name='order-product'),
    path('profile/', views.profile_page, name='profile'),
    path('orders/', views.order_history, name='orders'),
    path('process-order/<int:id>/', views.process_order, name='process-order'),
    path('update-order/<int:id>/', views.update_order, name='update-order'),
    path('delete-order/<int:id>/', views.delete_order, name='delete-order'),
]