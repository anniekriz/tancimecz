from django.contrib import admin
from django import forms
from .models import Event, Lector, Location

#admin.site.register(Event)
#admin.site.register(Lector)
admin.site.register(Location)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'display_lectors')
    change_form_template = 'admin/change_form.html'

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser: 
            form.base_fields['slug'].widget = forms.HiddenInput()
        return form

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
    change_form_template = 'admin/change_form.html'

    def get_form(self, request, obj=None, **kwargs):
        form = super(LectorAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser: 
            form.base_fields['user'].widget = forms.HiddenInput()
            form.base_fields['slug'].widget = forms.HiddenInput()
        return form

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



