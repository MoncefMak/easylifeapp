from django.contrib import admin

from core.models import Country, City


# Register your models here.
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'code']
    search_fields = ['name', 'code', 'country__name', 'country__code']
