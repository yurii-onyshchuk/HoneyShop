from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, Review
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label='Вміст', widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    list_display = ('id', 'title', 'price', 'category', 'available', 'created_at', 'get_photo')
    list_display_links = ('id', 'title',)
    list_filter = ('category', 'available',)
    search_fields = ('title',)
    fields = ('title', 'slug', 'price', 'available', 'category', 'description', 'photo', 'get_photo', 'sales', 'views',
              'created_at', 'users_wishlist')
    readonly_fields = ('created_at', 'views', 'sales', 'get_photo', 'users_wishlist')
    form = ProductAdminForm

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<a href="{obj.photo.url}"><img src="{obj.photo.url}" width="80"></a>')
        return '-'

    get_photo.short_description = 'Мініатюра'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'parent', 'body', 'created_at', 'user')
    list_display_links = ('id',)
    list_filter = ('product', 'user')
    search_fields = ('body',)
    fields = ('product', 'parent', 'body', 'created_at', 'user',)
    readonly_fields = ('created_at',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
