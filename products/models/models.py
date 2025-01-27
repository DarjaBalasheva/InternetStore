import uuid

from django.db import models

# У товара должно быть название, описание, картинка, цена, характеристики.
# Также необходимо иметь возможность фильтровать и сортировать по цене
# (не менее заданного значения и не более заданного значения)


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=100, null=False)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )  # Родительская категория


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    characteristics = models.JSONField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(default="")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        default="29b5de09-979a-47d5-a988-a4678cd8bdde",
    )


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartItem")

    def __str__(self):
        return f"Корзина пользователя {self.user.id}"


# Сколько товара храним в корзине
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в корзине {self.cart.user.id}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="OrderItem")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Заказ {self.id} пользователя {self.user.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в заказе {self.order.id}"
