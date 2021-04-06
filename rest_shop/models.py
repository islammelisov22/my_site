from django.core.validators import MaxValueValidator
from django.db import models


class Kit(models.Model):
    total_before = models.CharField(max_length=100)
    total_after = models.CharField(max_length=100)
    items = models.CharField(max_length=100, verbose_name='Введите товар', help_text='Товар')
    percent = models.ManyToManyField(validators=[MaxValueValidator])

# Create your models here.
