
from django.db import models
from product.models import Product

class TrackClick(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="clicks")
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.product.name} - {self.action} at {self.timestamp}"
