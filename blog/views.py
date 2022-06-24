from ast import keyword
import json
import os
import re
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import RegisterUserForm,LoginUserForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login
from .models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import blog.mongo_utils
from pymongo import MongoClient



def homepage(request):
    categorys = blog.mongo_utils.get_all({},'Categorys')
    print(categorys)
    return render(request, 'blog/homepage.html',{'categorys':categorys})
    
def get_categorys(request,category_id):
    products = blog.mongo_utils.get_all({'category':category_id},'Product')
    print(products)
    return render(request, 'blog/get_categorys.html',{'products':products})
def search(request):
    keyword = request.GET.get('keyword','')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    category = request.GET.get('category')

    filter_product = {'name':re.compile(f'.*{keyword}.*', re.IGNORECASE)}
    if price_to is not None and price_from is not None:
        filter_product.update({'$and':[{'price':{'$gt':price_from}},{'price':{'$lt':price_to}}]})
    else:
        if price_from is not None:
            filter_product.update({'price':{'$gt':int(price_from)}})
        if price_to is not None:
            filter_product.update({'price':{'$lt':int(price_to)}})
    if category is not None:
        filter_product.update({'category':category})
    filtered_product = blog.mongo_utils.get_all(filter_product,'Product')
    print(filtered_product)
    return render(request, 'blog/search.html',{'filtered_product':filtered_product})


def basket(request,id_prod):
    basket_data = request.session.get('baskett', {})
    count = basket_data.get(str(id_prod),0)
    basket_data[str(id_prod)] = count + 1
    request.session['baskett'] = basket_data
    print(request.session['baskett'])
    return redirect('/checkout')


@login_required(login_url='/login') #только для зарегествированных пользователей
def checkout(request):
    # users = User.objects.all()[0].id #получить id пользователей
    # print(users)
    basket_data = request.session.get('baskett', {})
    request.user.id # получаем текущий айди пользователя
    user_id = request.user.id
    print(user_id)
    basket_data.update({'user_id':user_id})
    print(basket_data)
    with open('file.json','w') as file:
        json.dump(basket_data,file)
    blog.mongo_utils.write_data(basket_data,'purcheses')
    return HttpResponse(f'Hello {basket_data}')
    


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