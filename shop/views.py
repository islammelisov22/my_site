from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import SearchForm, LoginForm, RegisterForm, EditForm
from .models import Dish, Category


def view_category(request):
    category_id = request.GET.get("category_id")
    category = Category.objects.filter(id=category_id)
    return render(request, 'category.html', {'category': category})


def add_dish(request):
    some_dish = Dish(title='рамен2', image='img.jpg', price=500, )
    some_dish.save()

    Dish.objects.create(title='рамен', image=' ', price=500, )
    return redirect('index')


def view_dishes(request):
    all_dishes = Dish.objects.all()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        search = request.POST.get('search')
        if form.is_valid() and search:
            all_dishes = all_dishes.filter(title__contains=search)
    else:
        form = SearchForm()

    return render(request, 'base.html',
                  {'dishes': all_dishes, 'form': form, 'user': request.user})


def edit_profile(request):
    if request.method == 'POST':
        form = EditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EditForm(instance=request.user)
    return render(request, 'login.html', {'form': form,'submit_text':'Изменить','auth_header':'Изменение профиля'})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # if request.GET and 'next' in request.GET:
                #     return redirect(request.GET['next'])
                return redirect('/')
            else:
                form.add_error('login', 'Bad login or password')
                form.add_error('password', 'Bad login or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'submit_text': 'Войти', 'auth_header': 'Вход'})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'login.html',
                  {'form': form, 'submit_text': 'Зарегистрироваться', 'auth_header': 'Регистрация'})


def log_out(request):
    logout(request)
    return redirect('/')
