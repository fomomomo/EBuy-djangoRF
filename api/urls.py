from django.urls import path
from . import views
urlpatterns = [

    path('', views.apiOverview, name='apiOverview'),
    path('products/', views.productList, name='products'),
    path('order-details/', views.orderDetails, name='order-details'),
    path('cart-item-list/', views.cartItemList, name='cart-item-list'),
    path('cart-update-item/<str:action>/<str:pk>', views.cartUpdateItem, name='cart-update-item'),   
    path('process-order/', views.processOrder, name='process-order'),       
]