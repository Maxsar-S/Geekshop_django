from django.urls import path

from mainapp.views import products, products_ajax
from django.views.decorators.cache import cache_page

app_name = 'mainapp'



urlpatterns = [
    path('', products, name='index'),
    path('<int:category_id>/', products, name='product'),
    path('page/<int:page>/', products, name='page'),
    path('<int:category_id>/', cache_page(3600) (products_ajax), name='product'),
    path('page/<int:page>/', cache_page(3600)(products_ajax), name='product'),
]