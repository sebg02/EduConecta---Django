from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import TeacherProfile, StudentProfile, Location, Classes


# Extensión de la clase UserAdmin (para gestionar los usuarios en el dashboard)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')

    def get_role(self, obj):
        return obj.userprofile.role if hasattr(obj, 'userprofile') else 'Sin perfil'
    
    get_role.short_description = 'Rol'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(Location)
admin.site.register(Classes)
