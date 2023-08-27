from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200,blank=False)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #quantity
    #image_url
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name[:20]
    
    class Meta:
        ordering = ['-updated','-created']


class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    #quantity = models.IntegerField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
    
    class Meta:
        ordering = ['updated','created']
