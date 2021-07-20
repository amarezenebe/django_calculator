from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form=UserChangeForm
    # add_form=RegistrationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display=(
        "nick", "first_name", "last_name", 'is_admin', "is_active", "id")
    list_filter=('is_admin',)
    fieldsets=(
        (None, {'fields': ('password',)}),
        ('Personal info', {'fields': ("nick", "first_name", "last_name",)}),
        ('Permissions', {'fields': ('is_admin', "is_active")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    search_fields=('nick',)
    ordering=('nick',)
    filter_horizontal=()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
