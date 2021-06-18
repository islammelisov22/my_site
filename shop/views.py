from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from .forms import SearchForm, LoginForm, RegisterForm, EditForm
from .models import Dish, Category, Cart, CartContent, UserProfile
from django.conf import settings
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Dish


class MasterView(View):
    def get_cart_records(self, cart=None, response=None):
        cart = self.get_cart() if cart is None else cart
        if cart is not None:
            cart_records = CartContent.objects.filter(cart_id=cart.id)
        else:
            cart_records = []

        if response:
            response.set_cookie('cart_count', len(cart_records))
            return response

        return cart_records

    def get_cart(self):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
            except ObjectDoesNotExist:
                cart = Cart(user_id=user_id,
                            total_cost=0)
                cart.save()
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key
            try:
                cart = Cart.objects.get(session_key=session_key)
            except ObjectDoesNotExist:
                cart = Cart(session_key=session_key,
                            total_cost=0)
                cart.save()
        return cart


class HomeView(MasterView):
    all_dishes = Dish.objects.all()

    def get(self, request):
        profile = None
        if request.user.is_authenticated:
            profile = UserProfile.objects.filter(user=request.user).first()
        form = SearchForm()
        return render(request, 'base.html',
                      {'dishes': self.all_dishes, 'form': form, 'profile': profile})

    def post(self, request):
        form = SearchForm(request.POST)
        search = request.POST.get('search')
        if form.is_valid() and search:
            search_vector = SearchVector('title',
                                         'description',
                                         'categories__title',
                                         'company__title', )
            self.all_dishes = self.all_dishes.annotate(search=search_vector).filter(search=search)
        else:
            form = SearchForm()
        return render(request, 'base.html',
                      {'dishes': self.all_dishes, 'form': form, 'user': request.user})


def view_category(request):
    category_id = request.GET.get("category_id")
    category = Category.objects.filter(id=category_id)
    return render(request, 'category.html', {'category': category})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EditForm(instance=request.user)
    return render(request, 'login.html', {'form': form, 'submit_text': 'Изменить', 'auth_header': 'Изменение профиля'})


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
            form.is_active = True
            form.is_superuser = True
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'login.html',
                  {'form': form, 'submit_text': 'Зарегистрироваться', 'auth_header': 'Регистрация'})


def log_out(request):
    logout(request)
    return redirect('/')


class CartView(MasterView):
    def get(self, request):
        cart = self.get_cart()
        cart_records = self.get_cart_records(cart)
        cart_total = cart.get_total() if cart else 0

        context = {
            'cart_records': cart_records,
            'cart_total': cart_total,
        }
        return render(request, 'cart.html', context)

    def post(self, request):
        dish = Dish.objects.get(id=request.POST.get('dish_id'))
        cart = self.get_cart()
        quantity = request.POST.get('qty')
        # get_or_create - найдет обьект, если его нет в базе, то создаст
        # первый параметр - обьект, второй - булевое значение которое сообщает создан ли обьект
        # если обьект создан, то True, если он уже имеется в базе, то False
        cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=dish)
        cart_content.qty = quantity
        cart_content.save()
        response = self.get_cart_records(cart, redirect('/#dish-{}'.format(dish.id)))
        return response


class DeleteCartView(MasterView):
    def remove(self, product):
        """
        Удаляем товар
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        # получаем общую стоимость
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # очищаем корзину в сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Dish, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
# Create your views here.