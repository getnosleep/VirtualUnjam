"""[Docstring] Registers models to django admin."""
from django.contrib import admin
from .models import Truck
# Register your models here.
admin.site.register(Truck)