from django.contrib import admin
from .models import Event, Lector, Location

#admin.site.register(Event)
#admin.site.register(Lector)
admin.site.register(Location)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'display_lectors')
    filter_horizontal = ('lector',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            lector = Lector.objects.get(user=request.user)
            return qs.filter(lector=lector)
        except Lector.DoesNotExist:
            return qs.none()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Only modify on creation
            try:
                lector = Lector.objects.get(user=request.user)
                obj.lector.add(lector)
            except Lector.DoesNotExist:
                pass

    def display_lectors(self, obj):
        return ", ".join([f"{lector.firstName} {lector.lastName}" for lector in obj.lector.all()])
    display_lectors.short_description = 'Lectors'

admin.site.register(Event, EventAdmin)

class LectorAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            lector = Lector.objects.get(user=request.user)
            return qs.filter(id=lector.id)
        except Lector.DoesNotExist:
            return qs.none()

admin.site.register(Lector, LectorAdmin)



