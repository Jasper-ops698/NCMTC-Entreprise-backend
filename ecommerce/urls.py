from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    # Add your ecommerce URL patterns here
    # Example:
    # path('products/', views.product_list, name='product_list'),
    path('test/', views.test_view, name='test'),
]
