from django.http import JsonResponse
from django.views import View

from ..models.models import Category


class CategoryListView(View):
    # renderer_classes = [UTF8JSONRenderer]

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent__isnull=True)  # Корневые категории
        category_data = self.get_categories_data(categories)
        return JsonResponse(category_data, safe=False)

    def get_categories_data(self, categories):
        category_data = []
        for category in categories:
            children = Category.objects.filter(parent=category)
            category_data.append(
                {
                    "id": category.id,
                    "name": category.name,
                    "children": self.get_categories_data(
                        children
                    ),  # Рекурсивно для дочерних категорий
                }
            )
        return category_data
