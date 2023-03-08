from django.contrib import admin

from main.models import Client, Loan, Payment

# Register your models here.
admin.site.register(Client)
admin.site.register(Loan)
admin.site.register(Payment)