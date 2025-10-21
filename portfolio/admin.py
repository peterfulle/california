from django.contrib import admin
from .models import Category, Technology, Project, ProjectImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'completed_date', 'featured')
    list_filter = ('category', 'featured', 'technologies')
    search_fields = ('title', 'description', 'client')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
