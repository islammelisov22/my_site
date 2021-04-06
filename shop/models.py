from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    # avatar

    def __str__(self):
        return self.user.username


class Company(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Category(models.Model):
    # CharField, IntegerField FloatField и другие- это поля модели
    title = models.CharField(max_length=100, verbose_name='Название Категории', help_text='введите название Категория')
    description = models.CharField(max_length=500, verbose_name='Описание')

    # возвращение дефолтного значения при обращении к обьекту

    def __str__(self):
        return self.title

    # Изменение заголовка модели в админке
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


# Модель блюда со своими полями и методами
class Dish(models.Model):
    # CharField, IntegerField FloatField и другие- это поля модели
    image = models.ImageField(upload_to='images/', blank=True, verbose_name='Картинка')
    title = models.CharField(max_length=100, verbose_name='Название блюда', help_text='введите название блюда')
    # связь многие ко многим позволяет связывать множество категорий с множеством товаров
    categories = models.ManyToManyField(Category, verbose_name='категория', )
    company = models.ForeignKey(Company, verbose_name='компания', on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=500, verbose_name='Описание')
    # цена не может быть ниже 0, поэтому используется PositiveIntegerField
    price = models.PositiveIntegerField(verbose_name='цена')

    # для корректного отображения категорий
    def get_categories(self):
        self.short_description = "Категории"
        return ', '.join([cat.title for cat in self.categories.all()])

    # возвращение дефолтного значения при обращении к обьекту
    def __str__(self):
        return self.title

    # Изменение заголовка модели в админке
    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
