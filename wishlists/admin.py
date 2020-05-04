from django.contrib import admin
from wishlists.models import WishList, Line


class LineInline(admin.TabularInline):
    model = Line


class WishListAdmin(admin.ModelAdmin):
    list_display = ('hash_id','owner','date_created')
    inlines = [LineInline]


admin.site.register(WishList,WishListAdmin)
admin.site.register(Line)