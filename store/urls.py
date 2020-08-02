from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('login/', views.loginUser, name="login"),
    path('logout/',views.logoutUser, name='logout'),
    path('register/', views.register, name="register"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="updateItem"),
    path('process_order/', views.processOrder, name="processOrder")
]