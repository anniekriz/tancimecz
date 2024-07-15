from django.contrib import admin
from .models import Event, Lector, Location

#admin.site.register(Event)
admin.site.register(Lector)
#admin.site.register(Location)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'lector')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            # Assuming each User has a corresponding Lector profile
            lector = Lector.objects.get(user=request.user)
            return qs.filter(lector=lector)
        except Lector.DoesNotExist:
            return qs.none()

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set the lector during the first save.
            try:
                obj.lector = Lector.objects.get(user=request.user)
            except Lector.DoesNotExist:
                pass  # Handle the case where the user does not have a corresponding Lector
        super().save_model(request, obj, form, change)

admin.site.register(Event, EventAdmin)




