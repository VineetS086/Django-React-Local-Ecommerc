from django.contrib import admin
from .models import Brand, ContactLens, Glasses, Product


admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ContactLens)
admin.site.register(Glasses)