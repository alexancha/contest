from django.contrib import admin
from guides.models import Tag


class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Tag, TagsAdmin)
