from django.contrib import admin

# Register your models here.

from django.utils.safestring import mark_safe

from .models import *


class AppAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "title",
        "cat",
        "time_create",
        "get_html_photo",
        "is_published",
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    list_filter = ("is_published", "time_create")
    prepopulated_fields = {"slug": ("title",)}
    fields = (
        "user",
        "title",
        "slug",
        "cat",
        "content",
        "link",
        "photo",
        "get_html_photo",
        "is_published",
        "time_create",
        "time_update",
    )
    readonly_fields = ("time_create", "time_update", "get_html_photo")
    save_on_top = True

    ordering = ["id"]

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Pic"




class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class FeedBackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "first_name",
        "last_name",
        "email",
        "shotter",
        "time_create",
    )
    list_display_links = ("id",)
    search_fields = ("user", "content", "email")
    readonly_fields = ("time_create", "shotter")
    fields = (
        "user",
        "first_name",
        "last_name",
        "email",
        "time_create",
        "content",
        "shotter",
    )
    save_on_top = True

    ordering = ["id"]

    def shotter(self, object):
        if object.content:
            return object.content[:50]+'...'

admin.site.register(Item, AppAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(FeedBack, FeedBackAdmin)
