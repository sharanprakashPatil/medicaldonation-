from django.contrib import admin
from .models import MedicalBlog

@admin.register(MedicalBlog)
class MedicalBlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'published_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'content']
