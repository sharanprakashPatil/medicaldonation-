from django.db import models

class MedicalBlog(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    source = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
