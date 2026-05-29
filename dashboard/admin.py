from django.contrib import admin
from .models import MedicalBlog

@admin.register(MedicalBlog)
class MedicalBlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'published_at', 'is_active', 'has_image']
    list_filter = ['is_active']
    search_fields = ['title', 'content']
    fieldsets = [
        ('Blog Info', {'fields': ['title', 'content', 'source']}),
        ('Media', {'fields': ['image', 'image_url']}),
        ('Status', {'fields': ['is_active']}),
    ]

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'
