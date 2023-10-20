from django.contrib import admin
from .models import Profile, AdminProfile, OrganizationProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .forms import ProfileCreationForm, ProfileChangeForm


class AdminsAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'first_name', 'position', 'email')
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    model = Profile

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(is_staff=True)
        return qs


class OrganizationsAdmin(admin.ModelAdmin):
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    model = Profile
    list_display = ('created_at', 'first_name', 'position', 'email', 'university_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', )}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(role="organization")
        return qs


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
admin.site.unregister(Group)
