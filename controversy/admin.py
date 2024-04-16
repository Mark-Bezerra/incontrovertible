from django.contrib import admin

# Register your models here.
from .models import Controversy
from .models import Data_Point

class ConstroversyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",),}

class PointAdmin(admin.ModelAdmin):
    pass


admin.site.register(Controversy, ConstroversyAdmin)
admin.site.register(Data_Point, PointAdmin)