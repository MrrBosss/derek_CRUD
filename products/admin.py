# Register your models here.
from django.contrib import admin
from .models import Product, ProductWeight, FAQ, Banner, Brand, Category, Order, ProductPrice
from .models import ProductColor, Catalog, OrderItem, Team, BestSeller, ProductShots


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','order_date', 'get_total_quantity']
    list_display_links = ['id','order_date']
    inlines = [OrderItemInline]

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())

    get_total_quantity.short_description = 'Total Quantity'


class ProductShotsInline(admin.TabularInline):
    model = ProductShots
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category',]
    search_fields = ['title']
    list_filter = ['category']
    autocomplete_fields = ('price',)
    raw_id_fields = ('price',)
    inlines = [ProductShotsInline]


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ['guid', 'amount', 'weight', 'color', 'stock']
    search_fields = ['weight__mass', 'color__name']
    autocomplete_fields = ('weight', 'color')
    raw_id_fields = ('weight', 'color')
    list_select_related = ['weight', 'color']


@admin.register(BestSeller)
class BestSellerAdmin(admin.ModelAdmin):
    list_display = ['id','product']
    list_display_links = ['id','product']

admin.site.register(Catalog)

@admin.register(ProductWeight)
class ProductWeightAdmin(admin.ModelAdmin):
    list_display = ['mass']
    search_fields = ['mass']


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'id']
    list_display_links = ['name', 'parent']
    search_fields = ['name']


admin.site.register(FAQ)

admin.site.register(Banner)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id','category','brands']
    list_display_links = ['id','category']
    search_fields = ['id']

admin.site.register(Team)
