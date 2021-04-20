from django.shortcuts import render

# Create your views here.
# функцию = контроллеры = вьюхи

def index(request):
    return render(request, 'mainapp/index.html')


def products(request):
    return render(request, 'mainapp/products.html')