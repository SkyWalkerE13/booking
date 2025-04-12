from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    image = models.ImageField(upload_to='hotels/', blank=True, null=True, verbose_name="Изображение отеля")

    def __str__(self):
        return self.name

    # ... остальной код ... 