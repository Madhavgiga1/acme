from django.db import models

# Create your models here.

class Product(models.Model):
    sku = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.sku = self.sku.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sku

class Webhook(models.Model):
    url = models.URLField()
    event_type = models.CharField(max_length=50, default='product.import')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.url