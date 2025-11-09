from django.contrib import admin
from .forms import StockCreateForm

# Register your models here.

from .models import *


class StockCreateAdmin(admin.ModelAdmin):
	list_display = ['catégorie', 'nom', 'quantité']
	form = StockCreateForm
	list_filter = ['catégorie']
	search_fields = ['catégorie', 'nom']


admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Catégorie)

