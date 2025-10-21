from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Technology(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="Nombre del icono o clase CSS")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Technologies"

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    client = models.CharField(max_length=200, blank=True)
    completed_date = models.DateField()
    image = models.ImageField(upload_to='projects/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    technologies = models.ManyToManyField(Technology)
    url = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-completed_date']

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.project.title} - Image {self.order}"
    
    class Meta:
        ordering = ['order']
