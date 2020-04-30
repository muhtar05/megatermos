from django.contrib import admin
from core.models import Menu, Settings, Carousel, Page


class PageInline(admin.TabularInline):
    model = Page


class MenuAdmin(admin.ModelAdmin):
    list_display = ('title','url')


class CarouselAdmin(admin.ModelAdmin):
    list_display = ('name','position')


class PageAdmin(admin.ModelAdmin):
    list_display = ('pk','menu')


admin.site.register(Menu,MenuAdmin)
admin.site.register(Settings)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Page, PageAdmin)


