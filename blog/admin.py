from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(label='Вміст', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True
    list_display = ('id', 'title', 'category', 'created_at', 'views', 'get_photo',)
    list_display_links = ('id', 'title',)
    list_filter = ('category',)
    search_fields = ('title',)
    fields = ('title', 'slug', 'category', 'content', 'photo', 'get_photo', 'views', 'created_at',)
    readonly_fields = ('created_at', 'views', 'get_photo',)
    form = PostAdminForm

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<a href="{obj.photo.url}"><img src="{obj.photo.url}" width="80"></a>')
        return '-'

    get_photo.short_description = 'Мініатюра'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
