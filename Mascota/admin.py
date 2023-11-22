from django.contrib import admin
from .models import Mascota


class MascotaAdmin(admin.ModelAdmin):
    readonly_fields = ('fechaIngreso',)
# Register your models here.

admin.site.register(Mascota, MascotaAdmin)
