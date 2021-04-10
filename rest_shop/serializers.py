from django.contrib.auth.models import User, Group
from rest_framework import serializers
from shop.models import Dish, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['url', 'id', 'title']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['url', 'id', 'title']


class DishSerializer(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True)
    # company = CompanySerializer(required=False)
    depth = 2

    class Meta:
        model = Dish
        fields = '__all__'

    def create(self, validated_data):
        categories = validated_data.pop("categories", [])
        instance = Dish.objects.create(**validated_data)
        for category in categories:
            instance.categories.add(category)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        categories = validated_data.pop("categories", [])
        instance = super().update(instance, validated_data)
        for category in categories:
            instance.categories.add(category)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']