from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account

class AccountAdmin(UserAdmin):
    list_display    = ('name', 'email', 'is_active', 'is_superuser')
    search_fields   = ('name', 'email')

    readonly_fields = ('date_joined', 'last_login', 'student_discount_date')
    exclude     = ('unique_key', )
    ordering    = ['name']

    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()


admin.site.register(Account, AccountAdmin)

