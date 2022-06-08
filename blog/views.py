from itertools import count
import json
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import RegisterUserForm,LoginUserForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login
from .models import Category,Product
import pickle


def homepage(request):
    categorys = Category.objects.all()
    return render(request, 'blog/homepage.html',{'categorys':categorys})
# def get_categorys(request,category_id):#принимаем category_id с urls.py
#     products = Product.objects.filter(available = True,category = category_id)
#     return render(request, 'blog/get_categorys.html',{'products':products})
def get_categorys(request,category_slug):
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'blog/get_categorys.html',{'products':products})
def basket(request,id_prod):
    basket_data = request.session.get('basket', {})
    count = basket_data.get(str(id_prod),0)
    basket_data[str(id_prod)] = count + 1
    request.session['basket'] = basket_data
    print(request.session['basket'])

    return render(request, 'blog/get_categorys.html')

def checkout(request):
    basket_data = request.session.get('basket', {})
    print(basket_data)
    with open('file.json','w') as file:
        json.dump(basket_data,file)
    return HttpResponse(f'Hello')
    


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_success_url(self):
        return reverse_lazy('homepage')


def logout_user(request):
    logout(request)
    return redirect('login')