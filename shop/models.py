from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shop:item_list_by_category',
                       args=[self.slug])

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category,
                                related_name='items',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length = 200, db_index=True)
    slug = models.SlugField(max_length = 200, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    #using decimal for prices to avoid rounding issue
    in_stock = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        #for queries involving id and slug
        

    def get_absolute_url(self):
        return reverse('shop:item_detail', 
                       args=[self. id, self.slug])

    def __str__(self):
        return self.name
    
    
    
    
    
    
    
    
