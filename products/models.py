import random
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q

User = settings.AUTH_USER_MODEL  # auth.user

TAGS_MODELS_VALUES = ['electronics', 'cars', 'boats', 'movies', 'cameras']


class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


class ProductColor(models.Model):
    name = models.CharField(max_length=150)
    color = models.CharField(max_length=60)


class FAQ(models.Model):
    question = models.CharField(max_length=500, null=True)
    answer = models.CharField(max_length=500, null=True)

    def __str__(self):
        return str(self.question)


class Banner(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to="banners", null=True)
    title = models.CharField(max_length=500, null=True)
    subtitle = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=250, null=True)


class Brand(models.Model):
    brands = models.ImageField(upload_to="products", null=True)
    name = models.CharField(max_length=500, null=True,blank=True)

    def __str__(self):
        return str(self.brands)


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def is_subcategory(self):
        """Returns True if the category is a subcategory."""
        return self.parent is not None

    def get_subcategories(self):
        """Returns a QuerySet of subcategories for the current category."""
        return self.subcategories.all()


class Catalog(models.Model):
    catalog = models.FileField(upload_to='products')


class Team(models.Model):
    name = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='images', null=True)
    position = models.CharField(max_length=50, null=True)


class ProductWeight(models.Model):
    mass = models.IntegerField(default=0, null=True, blank=True)


class Product(models.Model):
    title = models.CharField(max_length=255, null=True)
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=100)
    public = models.BooleanField(default=True)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    weight = models.ManyToManyField(ProductWeight)
    color = models.ManyToManyField(ProductColor)
    artikul = models.CharField(max_length=20)
    # color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    stock = models.IntegerField(verbose_name="Ostatka", default=0)
    ch_name = models.CharField(max_length=50, verbose_name='Xarakteristika nomi', null=True, blank=True)
    ch_value = models.CharField(max_length=50, verbose_name='Xarakteristika qiymati', null=True, blank=True)


    def calculate_price(self, selected_weight):
        """
        Calculate the price of the product based on the selected weight.
        """
        base_weight = 30  # Base weight in grams for the default price
        base_price = self.price

        # Calculate price per gram
        price_per_gram = base_price / base_weight

        # Adjust the price based on the selected weight
        final_price = price_per_gram * selected_weight.mass

        return round(final_price, 2)

    def get_absolute_url(self):
        return f"/api/products/{self.pk}/"

    def __str__(self) -> str:
        return str(self.title)

    @property
    def endpoint(self):
        return self.get_absolute_url()

    @property
    def path(self):
        return f"/products/{self.pk}/"

    @property
    def body(self):
        return self.description

    def search_products(query=None):
        products = Product.objects.all()

        if query:
            products = products.filter(title__icontains=query)

        # Order by product group sequence, then by title
        products = products.order_by('group__sequence', 'title')

        return products


class BestSeller(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True, null=True)
    name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    # Add other fields like customer information, shipping details, etc.


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=20, null=True)
    weight = models.IntegerField(null=True)
    quantity = models.IntegerField(default=0)

    @property
    def subtotal(self):
        return self.quantity * self.product.price

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.order.items.all())
