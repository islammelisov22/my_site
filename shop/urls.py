from django.urls import path

from shop import views

urlpatterns = [
    path('add/', views.add_dish, name="add"),
    path('index/', views.view_dishes, name="index"),
    path('edit/', views.edit_profile, name="edit"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('register/', views.register, name="register"),
]
