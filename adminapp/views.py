from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from authapp.models import User
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductEditForm, ProductCategoryEditForm
from mainapp.models import ProductCategory, Product

from django.db.models import F
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection

@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'adminapp/admin.html')


# CRUD - Create Read Update Delete
class UserListView(ListView):
    model = User
    template_name = 'adminapp/admin-users-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admin_staff:admin_users_read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users_read')
    form_class = UserAdminProfileForm

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop Admin - Редактирование пользователя'
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)





class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesListView, self).dispatch(request, *args, **kwargs)


class CategoriesCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-create.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin_staff:admin-categories-read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesCreateView, self).dispatch(request, *args, **kwargs)


class CategoriesUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin-categories-read')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'GeekShop Admin - Редактирование категории'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'Применяется скидка {discount}% к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price') * (1- discount/100))
                # db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)



class CategoriesDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin-categories-read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)






class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/admin-products-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductListView, self).dispatch(request, *args, **kwargs)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/admin-products-create.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('admin_staff:admin-products-read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCreateView, self).dispatch(request, *args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/admin-products-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin-products-read')
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop Admin - Редактирование категории'
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/admin-products-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin-products-read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)