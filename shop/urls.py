
from django.urls import path
from shop import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="index"),
    path('category/', views.view_category, name="category"),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/', views.DeleteCartView.as_view(), name='delete_from_cart'),
    # user actions
    path('edit/', views.edit_profile, name="edit"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name='log_out'),
    path('register/', views.register, name="register"),
    path('remove/<int:product_id>/', views.DeleteCartView.as_view, name='cart_remove'),

]
