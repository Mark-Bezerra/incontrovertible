from django.db import models
from django.conf import settings
from django.urls import reverse

DATA_SETS = (
    ('data','DATA'),
    ('opinion','OPINION'),
    ('advice','ADVICE'),
)

class Controversy(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="")
    slug = models.SlugField(null=False, unique=True, default="")
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("controversy:detail", args=[str(self.slug)])

class Data_Point(models.Model):
    controversy = models.ForeignKey(Controversy, on_delete=models.PROTECT, related_name="points")
    name = models.CharField(max_length=32)
    description = models.TextField(default="")
    url = models.URLField()
    data_set = models.CharField(max_length=16, choices=DATA_SETS, default='data')
    boolean = models.BooleanField()
