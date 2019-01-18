from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/', views.detail, name='detail'),
]
