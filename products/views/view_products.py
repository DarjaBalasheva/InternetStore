from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response

from ..models.models import User, Product, Category
from django.views import View
from django.http import HttpResponse
import json

from ..models.serializers import ProductSerializer
from ..renderens import UTF8JSONRenderer


class ProductListView(generics.ListAPIView):
    renderer_classes = [UTF8JSONRenderer]

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListByCategoryView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        category_id = request.data.get('category_id')

        if not category_id:
            return Response({"error": "Category ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(id=category_id)  # Получаем категорию из базы данных
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(category=category)  # Фильтруем товары по категории

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(View):
    renderer_classes = [UTF8JSONRenderer]

    def get(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['pk'])
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)