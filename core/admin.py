from django.contrib import admin
from .models import Category, Child, ClothingItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'birth_date', 'gender', 'get_age_display')
    list_filter = ('gender', 'parent')
    search_fields = ('name', 'parent__username')
    raw_id_fields = ('parent',)

    def get_age_display(self, obj):
        from django.utils import timezone
        import datetime
        today = timezone.now().date()
        born = obj.birth_date
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return f"{age} лет"
    get_age_display.short_description = "Возраст"


@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'child', 'category', 'size', 'season', 'condition', 'status', 'created_at')
    list_filter = ('season', 'condition', 'status', 'category', 'child')
    search_fields = ('name', 'child__name', 'notes')
    raw_id_fields = ('child', 'category')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    list_editable = ('status',)