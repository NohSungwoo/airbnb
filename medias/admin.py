from django.contrib import admin

from .models import Photo, Video


@admin.register(Photo)
class PhotoAmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAmin(admin.ModelAdmin):
    pass
