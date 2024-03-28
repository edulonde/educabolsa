from django.contrib import admin
from .models import RespostasQuestionarioInicial
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_answered')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_answered',)}),
    )


admin.site.register(RespostasQuestionarioInicial)
admin.site.register(CustomUser, CustomUserAdmin)