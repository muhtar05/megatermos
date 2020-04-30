from django.contrib import admin

from order.models import Order, Line


class LineInline(admin.TabularInline):
    model = Line
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'total_excl_tax', 'user', 'status','date_placed')


class LineAdmin(admin.ModelAdmin):
    list_display = ('order', 'product',  'quantity')


admin.site.register(Order, OrderAdmin)
admin.site.register(Line, LineAdmin)
