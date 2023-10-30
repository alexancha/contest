from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from users.models import Profile
from .models import Mootcourt


class MootcourtAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'title', 'get_organizer_link', 'event_type', 'status')
    list_display_links = ('created_at', 'title', 'event_type', 'status')
    # fields = ['created_at', 'title', 'organizer', 'event_type', 'tags', 'announcement', 'messages', 'events',
    #           'documents', 'need_telegram_channel', 'telegram_channel', 'teams', 'senior_referees', 'referees',
    #           'status_moot_court', 'background', 'image', 'status', 'display_on_main']

    def get_organizer_link(self, obj):
        if obj.organizer:
            if obj.organizer.role:
                if obj.organizer.role == "organization":
                    url = reverse('admin:users_organizationprofile_change', args=[obj.organizer.id])
                    return format_html('<a href="{}">{}</a>', url, obj.organizer.first_name)
                else:
                    url = reverse('admin:users_participantprofile_change', args=[obj.organizer.id])
                    return format_html('<a href="{}">{}</a>', url, obj.organizer.first_name)
            else:
                if obj.organizer.is_staff:
                    url = reverse('admin:users_adminprofile_change', args=[obj.organizer.id])
                    return format_html('<a href="{}">{}</a>', url, obj.organizer.first_name)
        return ''
    get_organizer_link.short_description = 'Organizer'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'senior_referees' or db_field.name == 'referees':
            kwargs['queryset'] = Profile.objects.filter(role="referee")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Mootcourt, MootcourtAdmin)