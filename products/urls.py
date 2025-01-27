from django.urls import path

from .views import view_products, views_catalog, views_categories

urlpatterns = [
    path(
        "product/<uuid:pk>/", view_products.ProductDetailView.as_view(), name="product"
    ),
    path(
        "products/all", view_products.ProductListView.as_view(), name="product-list"
    ),  # Для GET-запросов на список всех продуктов
    path(
        "products/",
        view_products.ProductListByCategoryView.as_view(),
        name="product-list-by-category",
    ),  # Для POST-запросов с фильтрацией по категории
    path(
        "categories/", views_categories.CategoryListView.as_view(), name="category-list"
    ),
    path("", views_catalog.index, name="index"),
]
