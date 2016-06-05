from django.contrib import admin

from .models import Gallery, GalleryImage

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage

class GalleryAdmin(admin.ModelAdmin):
    inlines = (GalleryImageInline,)
    readonly_fields = ('slug',)

admin.site.register(Gallery, GalleryAdmin)