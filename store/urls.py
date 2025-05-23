from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('phones/', views.phone_list, name='phone_list'),
    path('phones/<int:phone_id>/', views.phone_detail, name='phone_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:phone_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-quantity/<int:cart_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/summary/', views.cart_summary, name='cart_summary'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-complete/<int:order_id>/', views.order_complete, name='order_complete'),
    path('brands/', views.brand_list, name='brands'),
    path('brands/<int:brand_id>/', views.brand_detail, name='brand_detail'),
    path('search/', views.search, name='search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('checkout/', views.checkout, name='checkout'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/orders/<int:order_id>/update-status/', 
         views.update_order_status, name='update_order_status'),
]