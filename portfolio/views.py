from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Project, Category

class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener proyectos relacionados (misma categoría)
        context['related_projects'] = Project.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context
