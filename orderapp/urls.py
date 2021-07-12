from django.urls import path

import orderapp.views as orderapp

app_name = 'orderapp'

urlpatterns = [
    path('', orderapp.OrderList.as_view(), name='list'),
    path('create/', orderapp.OrderCreate.as_view(), name='create'),
    path('update/<int:pk>/', orderapp.OrderUpdate.as_view(), name='update'),
    path('read/<int:pk>/', orderapp.OrderRead.as_view(), name='read'),
    path('delete/<int:pk>/', orderapp.OrderDelete.as_view(), name='delete'),
    path('forming/complete/<int:pk>/', orderapp.forming_complete, name='forming_complete'),

    path('product/<int:pk>/price/', orderapp.get_product_price)

]