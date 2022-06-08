from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100,db_index=True)
    slug = models.SlugField(max_length=100,unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=150,db_index=True)
    slug = models.CharField(max_length=150,db_index=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    description = models.TextField(max_length=1000,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    available = models.BooleanField(default=True)#активность,отвечает за то что активный товар или нет
    created = models.DateTimeField(auto_now_add=True)#время добавления 
    uploaded = models.DateTimeField(auto_now=True)#время изменения

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id','slug'),)

    def __str__(self):
        return self.name
