from django.contrib import admin
from core.models import  Settings, Carousel, Page


class CarouselAdmin(admin.ModelAdmin):
    list_display = ('name','position')


class PageAdmin(admin.ModelAdmin):
    list_display = ('title','type','position')
    list_filter = ('type','is_menu_top','is_menu_footer')


admin.site.register(Settings)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Page, PageAdmin)


