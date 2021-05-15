from django.contrib import admin
from .models import Brand, ContactLens, Glasses, Product, Purchase, PurchaseItem, Review, Shipping


admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ContactLens)
admin.site.register(Glasses)
admin.site.register(Review)
admin.site.register(Shipping)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)