from django.urls import path

from adminapp.views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView, CategoriesUpdateView, \
    CategoriesListView, CategoriesCreateView, CategoriesDeleteView, ProductDeleteView, ProductUpdateView, \
    ProductCreateView, ProductListView

app_name = 'adminapp'

urlpatterns = [
    path('', index, name='index'),
    path('admin-users-read/', UserListView.as_view(), name='admin_users_read'),
    path('admin-users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('admin-users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('admin-users-remove/<int:pk>/', UserDeleteView.as_view(), name='admin_users_remove'),


    path('admin-categories-read/', CategoriesListView.as_view(), name='admin-categories-read'),
    path('admin-categories-create/', CategoriesCreateView.as_view(), name='admin-categories-create'),
    path('admin-categories-update/<int:pk>/', CategoriesUpdateView.as_view(), name='admin-categories-update'),
    path('admin-categories-remove/<int:pk>/', CategoriesDeleteView.as_view(), name='admin-categories-remove'),


    path('admin-products-read/', ProductListView.as_view(), name='admin-products-read'),
    path('admin-products-create/', ProductCreateView.as_view(), name='admin-products-create'),
    path('admin-products-update/<int:pk>/', ProductUpdateView.as_view(), name='admin-products-update'),
    path('admin-products-remove/<int:pk>/', ProductDeleteView.as_view(), name='admin-products-remove'),
]
