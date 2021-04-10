from django.contrib import admin
from .models import Dish, Category

admin.site.register(Category)

# регистрация модели в админке
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    # список отображаемых полей модели
    list_display = ['id', 'title', 'get_categories', 'description']
