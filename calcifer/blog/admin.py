
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from calcifer.blog.models import Post, PostFile
from calcifer.common.models import Tag, File


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class FileAdmin(admin.ModelAdmin):
    list_display  = ('file', 'thumbnail', 'get_size',
                     'mime', 'created', 'is_image')
    list_filter   = ('tags', 'is_image')
    readonly_fields = ('mime', 'size', 'width', 'height', 'is_image',
                       'created', 'modified')
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {
            'fields': ('file', 'alt', 'author', 'created', 'modified')
        }),
        (None, {
            'fields': ('mime', 'size',)
        }),
        (None, {
            'fields': ('is_image', 'width', 'height')
        }),
        (_('Tags'), {
            'classes': ('collapse',),
            'fields': ('tags',),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(FileAdmin, self).formfield_for_foreignkey(
                db_field, request, **kwargs)


class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display  = ('slug', 'title', 'author', 'publish', 'get_status')
    list_filter   = ('publish', 'tags', 'status', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (PostFileInline,)
    filter_horizontal = ('tags',)
    readonly_fields = ('created', 'modified')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'body', 'markup')
        }),
        (None, {
            'fields': ('publish', 'status', 'allow_comments')
        }),
        (None, {
            'fields': ('created', 'modified')
        }),
        (_('Tags'), {
            'classes': ('collapse',),
            'fields': ('tags',),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(PostAdmin, self).formfield_for_foreignkey(
                db_field, request, **kwargs)

    class Media:
        css = {'all': (
            'http://fonts.googleapis.com/css?family=Inconsolata',
            '/media/css/admin.css',
        )}


admin.site.register(Tag, TagAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Post, PostAdmin)

