from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Product, Review


class ProductAdminForm(forms.ModelForm):
    """Custom form for the Product admin."""

    description = forms.CharField(label='Опис', required=False, widget=CKEditorUploadingWidget())
    characteristic = forms.CharField(label='Характеристика', required=False, widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for managing products."""

    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    list_display = ('id', 'title', 'price', 'category', 'quantity', 'created_at', 'get_photo')
    list_display_links = ('id', 'title',)
    list_filter = ('category', 'quantity',)
    search_fields = ('title',)
    fields = ('title', 'slug', 'price', 'quantity', 'category', 'description', 'characteristic', 'photo', 'get_photo',
              'sales', 'views', 'created_at', 'users_wishlist')
    readonly_fields = ('created_at', 'views', 'sales', 'get_photo', 'users_wishlist')
    form = ProductAdminForm

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<a href="{obj.photo.url}"><img src="{obj.photo.url}" width="80"></a>')
        return '-'

    get_photo.short_description = 'Мініатюра'


class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for managing product categories."""

    prepopulated_fields = {'slug': ('title',)}


class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for managing product reviews."""

    list_display = ('id', 'body', 'parent', 'product', 'created_at', 'user',)
    list_display_links = ('id',)
    list_filter = ('user', 'product',)
    search_fields = ('body',)
    fields = ('body', 'parent', 'product', 'created_at', 'user',)
    readonly_fields = ('created_at',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
