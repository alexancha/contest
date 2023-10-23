from django.contrib import admin
from .models import Profile, AdminProfile, OrganizationProfile, ParticipantProfile, Team
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from .forms import ProfileCreationForm, ProfileChangeForm


class MyAdminSite(AdminSite):
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request, app_label)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())
        # Sort the models alphabetically within each app.
        # for app in app_list:
        #     app["models"].sort(key=lambda x: x["name"])
        return app_list


admin.site = MyAdminSite()


class AdminsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'created_at')
    fieldsets = (
        (None, {'fields': ('first_name', 'status', 'email')}),
        ('Permissions', {'fields': ('is_staff', )}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(is_staff=True)
        return qs


class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'first_name', 'position', 'email', 'university_name')
    fieldsets = (
        (None, {'fields': ('university_name', 'first_name', 'role', 'phone', 'email', 'verified_user', 'status')}),
    )
    list_filter = ['verified_user']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(role="organization")
        return qs


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'first_name', 'position', 'email')
    list_filter = ['role', 'status']
    search_fields = ('first_name', 'email',)
    fieldsets = (
        (None, {'fields': ('first_name', 'role', 'email', 'status')}),
    )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(role="participant") | qs.filter(role="coach") | qs.filter(role="referee")
        return qs


class TeamAdmin(admin.ModelAdmin):
    list_display = ('get_owner_name', 'name', 'created_at')
    fields = ['name', 'organization', 'verified_by_organization', 'status', 'coaches', 'owner']
    search_fields = ('owner__first_name', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(db_field.name)
        if db_field.name == 'organization':
            kwargs['queryset'] = Profile.objects.filter(role="organization").values_list('university_name', flat=True)
        if db_field.name == 'owner':
            kwargs['queryset'] = Profile.objects.filter(role="participant").values_list('first_name', flat=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        print(db_field.name)
        if db_field.name == 'coaches':
            kwargs['queryset'] = Profile.objects.filter(role="coach").values_list('first_name', flat=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


    def get_owner_name(self, obj):
        return obj.owner.first_name if obj.owner else ''

    get_owner_name.short_description = 'Owner Name'



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'first_name', 'position', 'email')
    list_filter = ('created_at', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'email')
    actions = ['make_inactive', 'make_active']


    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    def make_active(self, request, queryset):
        queryset.update(is_active=True)


admin.site.register(AdminProfile, AdminsAdmin)
admin.site.register(OrganizationProfile, OrganizationsAdmin)
admin.site.register(ParticipantProfile, ParticipantAdmin)
admin.site.register(Team, TeamAdmin)

