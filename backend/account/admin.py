from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account

class AccountAdmin(UserAdmin):
    list_display    = ('username', 'email', 'is_active', 'is_superuser')
    search_fields   = ('username', 'email')

    readonly_fields = ('date_joined', 'last_login', 'student_discount_date')
    exclude     = ['unique_key']
    ordering    = ['username']

    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()


admin.site.register(Account, AccountAdmin)

