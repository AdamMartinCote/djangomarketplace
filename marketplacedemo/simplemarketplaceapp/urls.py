from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('cart/', views.cart, name='cart'),
    path('purchase/', views.purchase, name='purchase'),
]
