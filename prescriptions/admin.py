# prescriptions/admin.py

from django.contrib import admin
from .models import Scan, Medicine

class MedicineInline(admin.TabularInline):
    model = Medicine
    extra = 1

@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username', 'extracted_text')
    inlines = [MedicineInline]

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'dosage', 'frequency', 'scan')
    list_filter = ('scan__user',)
    search_fields = ('name', 'description')