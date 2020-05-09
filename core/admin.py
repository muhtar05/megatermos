from django.contrib import admin
from core.models import  Settings, Carousel, Page, Region, City


class CarouselAdmin(admin.ModelAdmin):
    list_display = ('name','position')


class PageAdmin(admin.ModelAdmin):
    list_display = ('title','type','position')
    list_filter = ('type','is_menu_top','is_menu_footer')


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {"slug": ("name",)}


class CityAdmin(admin.ModelAdmin):
    list_display = ('name','shipping_price')
    list_filter = ('region',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Settings)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(City, CityAdmin)


