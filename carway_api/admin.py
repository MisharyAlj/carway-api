from django.contrib import admin
from .models import AdditionalServices, Invoice, WashType

# Register your models here.


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'date', 'time', 'total')

    search_fields = ('date',)
    ordering = ('-date',)


class WashTypeAdmin(admin.ModelAdmin):
    list_display = ('car_size', 'wash_type', 'price')

    search_fields = ('car_size',)
    ordering = ('car_size',)


class AdditionalServicesAdmin(admin.ModelAdmin):
    list_display = ('service', 'price')

    search_fields = ('service', 'price',)
    ordering = ('price',)


admin.site.register(WashType, WashTypeAdmin)
admin.site.register(AdditionalServices, AdditionalServicesAdmin)
admin.site.register(Invoice, InvoiceAdmin)
