from django.contrib import admin
from service.models import Document, Message, Event, Channel


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('created_at', )


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('created_at', )


class EventsAdmin(admin.ModelAdmin):
    list_display = ('created_at', )


class ChannelsAdmin(admin.ModelAdmin):
    list_display = ('created_at', )


admin.site.register(Document, DocumentsAdmin)
admin.site.register(Message, DocumentsAdmin)
admin.site.register(Event, DocumentsAdmin)
admin.site.register(Channel, DocumentsAdmin)
