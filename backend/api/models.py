from django.db import models
from account.models import Account


class Brand(models.Model):
    TYPE_CHOICE     = [
        ('B', 'Budget'),
        ('P', 'Premium'),
        ('S', 'Super Premiun')
    ]

    LOCATION_CHOICE = [
        ('N', 'National'),
        ('I', 'Inter National'),
        ('M', 'Multi National'),
    ]

    name        = models.CharField(max_length=32)
    # image   = models.ImageField()
    brand_type  = models.CharField(max_length=1, choices=TYPE_CHOICE)
    location    = models.CharField(max_length=1, choices=LOCATION_CHOICE)


    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name            = models.CharField(max_length=200)
    brand           = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    price           = models.DecimalField(max_digits=8, decimal_places=2)
    description     = models.TextField()
    count_in_stock  = models.PositiveSmallIntegerField()
    # image           = ImageField()
    added_at        = models.DateTimeField(auto_now_add=True)
    discount        = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_cod_available= models.BooleanField(default=True, verbose_name='COD Available')

    rating          = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    sales           = models.PositiveSmallIntegerField(default=0)
    # trendy_score    = models.

    def __str__(self) -> str:
        return f'{self.name}'


class ContactLens(models.Model):
    DISPOSABILITY_CHOICE    = [
        ('1D' , 'Single Day'),
        ('2W' , 'Two Weeks'),
        ('1M' , 'One Month'),
        ('3M' , 'Quater Year'),
        ('1Y' , 'One Year')
    ]

    POWERTYPE_CHOICE    = [
        ('1', 'type 1'),
        ('2', 'type 2')
    ]
    
    product         = models.OneToOneField(Product, on_delete=models.CASCADE)
    disposability   = models.CharField(max_length=2, choices=DISPOSABILITY_CHOICE)
    colur           = models.CharField(max_length=24, blank=True, null=True)
    base_curve      = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    diameter        = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    content_in_box  = models.PositiveSmallIntegerField(default=30)
    material        = models.CharField(max_length=32)
    power_type      = models.CharField(max_length=4, choices=POWERTYPE_CHOICE, blank=True, null=True)
    power_range_low = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    power_range_high= models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    

    class Meta:
        verbose_name        = "Contact Lens"
        verbose_name_plural = "Contact Lenses"

    def __str__(self) -> str:
        return f'{self.product}'


class Glasses(models.Model):
    GENDER_CHOICE   = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('U', 'Unisex'),
    ]
    PURPOSE_CHOICE  = [
        ('S', 'Sunglass'),
        ('C', 'Computer'),
        ('S', 'Reading Glasses'),
        ('N', 'Casual')
    ]
    MATERIAL_TYPE_CHOICE    = [
        ('M', 'Metalic'),
        ('P', 'Plastic'),
        ('B', 'Mixed'),
    ]

    product     = models.OneToOneField(Product, on_delete=models.CASCADE)
    gender      = models.CharField(max_length=1, choices=GENDER_CHOICE)
    is_for_kids = models.BooleanField(default=False)
    purpose     = models.CharField(max_length=10, choices=PURPOSE_CHOICE)
    material_type   = models.CharField(max_length=1, choices=MATERIAL_TYPE_CHOICE)
    frame_material  = models.CharField(max_length=64, null=True, blank=True)
    temple_material = models.CharField(max_length=64, null=True, blank=True)
    frame_style     = models.CharField(max_length=32, null=True, blank=True)
    frame_color     = models.CharField(max_length=32, null=True, blank=True)

    frame_width     = models.PositiveSmallIntegerField(null=True, blank=True)
    lens_height     = models.PositiveSmallIntegerField(null=True, blank=True)
    lens_weidth     = models.PositiveSmallIntegerField(null=True, blank=True)
    frame_weight    = models.PositiveSmallIntegerField(null=True, blank=True)
    
    prescription_type   = models.CharField(max_length=60, null=True, blank=True)
    power_range_low     = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    power_range_high    = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Glasses"

    
    def __str__(self) -> str:
        return f'{self.product}'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating  = models.PositiveSmallIntegerField()
    titel   = models.CharField(max_length=100)
    content = models.TextField()

    # class Meta:
    #     unique_together = ['product', 'account']

class Shipping(models.Model):
    SHIPPING_TYPE_CHOICE    = [
        ('COD', 'Cash On Delivery'),
        ('OP',  'Online Payment')
    ]

    type            = models.CharField(max_length=3, choices=SHIPPING_TYPE_CHOICE)
    shipping_cost   = models.DecimalField(max_digits=7, decimal_places=2)
    address         = models.CharField(max_length=200)
    pin             = models.CharField(max_length=6)
    city            = models.CharField(max_length=100)
    state           = models.CharField(max_length=100)

    
    @property
    def full_address(self):
        return f'{self.address}, {self.city}, {self.state}({self.pin})'

    def __str__(self) -> str:
        return self.full_address


class Purchase(models.Model):
    PURCHASE_STATE_CHOICE   = [
        ('C', 'Cart'),
        ('O', 'Order')
    ]
    account         = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    purchase_state  = models.CharField(max_length=1, choices=PURCHASE_STATE_CHOICE, default='C')
    payment_method  = models.CharField(max_length=30, null=True, blank=True)
    ordered_at      = models.DateTimeField(blank=True, null=True)
    is_completed    = models.BooleanField(default=False)
    shipping        = models.OneToOneField(Shipping, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self) -> str:
        return f'{self.account}->{self.purchase_state}'

    @property
    def purchase_total(self):
        items   = self.purchaseitem_set.all()
        return sum([item.item_total for item in items])
        


class PurchaseItem(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    = models.PositiveSmallIntegerField(default=1)
    purchase    = models.ForeignKey(Purchase, on_delete=models.CASCADE)

    class Meta:
        verbose_name        = "Purchase Item"
        verbose_name_plural = "Purchase Items"

    def __str__(self) -> str:
        return f'{self.product}'

    @property
    def item_total(self):
        return self.quantity*self.product.price