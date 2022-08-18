from django.contrib import admin
from .models import Product,Category,Cart,CartItem,Order,OrderItem,Review,Product2,feedback,Complited



admin.site.site_header="BOOT UP"
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)

admin.site.register(feedback)
admin.site.register(Complited)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20


admin.site.register(Product, ProductAdmin)

class ProductAdmin1(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20


admin.site.register(Product2, ProductAdmin1)


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fieldsets = [
        ('Product', {'fields': ['product'], }),
        ('Quantity', {'fields': ['quantity'], }),
        ('Price', {'fields': ['price'], }),
    ]
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False
    max_num = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'billingName', 'emailAddress', 'created','total','billingCity','status']
    list_filter=['created','total','billingCity','status']
    list_display_links = ('id', 'billingName')
    search_fields = ['id', 'billingName', 'emailAddress','created','total','billingCity']
    list_editable = ['status']

    fieldsets = [
        
        ('BILLING INFORMATION', {'fields': ['billingName', 'billingAddress1',
                                            'billingCity', 'billingPostcode', 'billingCountry', 'emailAddress']}),
        ('SHIPPING INFORMATION', {'fields': ['shippingName', 'shippingAddress1',
                                             'shippingCity', 'shippingPostcode', 'shippingCountry']}),
        ('status INFORMATION', {'fields': ['status']})
    ]
    def has_add_permission(self, request):
        return False
    inlines = [
        OrderItemAdmin,
    ]

    

   

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)
