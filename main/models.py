# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('shoes', 'Shoes'),
        ('gloves', 'Gloves'),
        ('socks', 'Socks'),
        ('ball', 'Ball'),
        ('cone', 'Cone'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    is_featured = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0)