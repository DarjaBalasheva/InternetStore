from rest_framework import serializers

from .models import Category, Product, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "firstname", "lastname"]


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "children"]  # Возвращаем id, name и дочерние категории

    def get_children(self, obj):
        """Получаем дочерние категории для текущей категории"""
        children = Category.objects.filter(parent=obj)
        return CategorySerializer(
            children, many=True
        ).data  # Рекурсивно сериализуем дочерние категории


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "characteristics",
            "image",
            "category",
        ]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "user", "products"]
