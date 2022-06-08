from django.contrib import admin

from .models import Category,Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug'] # указывает какие поля отображать на странице списка объектов.
    prepopulated_fields = {'slug': ('name',), }#афтозаполнение поля,>>
    # когда в админке пишем что-то в поле name афтоматически заполяеет slug с переводом

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price','available','created','uploaded']# указывает какие поля отображать на странице списка объектов.
    list_filter = ['available','created','uploaded']
    list_editable = ['price','available']#то что можно редактировать прям в админке
    prepopulated_fields = {'slug':('name',)}#афтозаполнение поля,>>
    # когда в админке пишем что-то в поле name афтоматически заполяеет slug с переводом