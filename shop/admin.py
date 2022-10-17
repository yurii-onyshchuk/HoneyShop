from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, Comment


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    list_display = ('id', 'title', 'price', 'category', 'available', 'created_at', 'get_photo')
    list_display_links = ('id', 'title',)
    list_filter = ('category', 'available',)
    search_fields = ('title',)
    fields = ('title', 'slug', 'price', 'available', 'category', 'description', 'photo', 'get_photo', 'sales', 'views', 'created_at',)
    readonly_fields = ('created_at', 'views', 'sales', 'get_photo',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<a href="{obj.photo.url}"><img src="{obj.photo.url}" width="80"></a>')
        return '-'

    get_photo.short_description = 'Мініатюра'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'body', 'created_at', 'user')
    list_display_links = ('id',)
    list_filter = ('product', 'user')
    search_fields = ('body',)
    fields = ('product', 'body', 'created_at', 'user',)
    readonly_fields = ('product', 'body', 'created_at', 'user',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
