from django.db import models


class Image(models.Model):
    image = models.ImageField()


class Category(models.Model):
    # parent = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_parent', null=True, blank=True)
    key = models.CharField(max_length=50)

    def __str__(self):
        return self.key


class Type(models.Model):
    key = models.CharField(max_length=50)

    def __str__(self):
        return self.key


class Option(models.Model):
    key = models.CharField(max_length=50)
    # value = models.CharField(max_length=30)

    def __str__(self):
        # return f'{self.key}: {self.value}'
        return self.key


class Item(models.Model):
    code = models.CharField(max_length=30, unique=True)
    images = models.ManyToManyField(Image, related_name='item_images')
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rent_price = models.PositiveIntegerField(null=True, blank=True)
    total_price = models.PositiveIntegerField()
    area = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='item_category')
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, related_name='item_type')
    options = models.ManyToManyField(Option, related_name='item_options', blank=True)
    notes = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    def short_description(self):
        return self.description[:20]

