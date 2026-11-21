from django.contrib import admin

from .models import Announcement, ReadStatus


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "published_date")
    list_filter = ("category",)
    search_fields = ("title", "body")
    list_select_related = ("author",)
    date_hierarchy = "published_date"


@admin.register(ReadStatus)
class ReadStatusAdmin(admin.ModelAdmin):
    list_display = ("student", "announcement", "read_at")
    list_filter = ("student",)
    list_select_related = ("student", "announcement")
