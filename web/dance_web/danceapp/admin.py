from django.contrib import admin
from django import forms
from .forms import EventGroupForm
from .widgets import CustomTimeWidget
from .models import Event, Lector, Location, EventGroup, Workshop
from django.utils.html import format_html

admin.site.register(Location)

class EventInline(admin.TabularInline):
    model = Event
    extra = 0  # Number of empty event forms to display

class EventGroupAdmin(admin.ModelAdmin):
    inlines = [EventInline]
    form = EventGroupForm  
    list_display = ('location', 'startTime', 'endTime', 'short_description')
    search_fields = ('location__name', 'description')

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventGroupAdmin, self).get_form(request, obj, **kwargs)
        return form
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(lector__user=request.user)

admin.site.register(EventGroup, EventGroupAdmin)

class EventAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_form.html'
    list_display = ('date', 'parent', 'description', 'get_end_time')  # Use method for endTime
    list_filter = ('date', 'parent')
    search_fields = ('description', 'parent__location__name')

    def get_end_time(self, obj):
        return obj.parent.endTime
    get_end_time.short_description = 'End Time'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            lector = Lector.objects.get(user=request.user)
            return qs.filter(parent__lector=lector)
        except Lector.DoesNotExist:
            return qs.none()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            try:
                lector = Lector.objects.get(user=request.user)
                obj.lector.add(lector)
            except Lector.DoesNotExist:
                pass

    def display_lectors(self, obj):
        return ", ".join([f"{lector.firstName} {lector.lastName or ''}" for lector in obj.lector.all()])
    display_lectors.short_description = 'Lectors'

admin.site.register(Event, EventAdmin)

admin.site.unregister(Event)

class WorkshopAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_form.html'
    list_display = ('title', 'title2', 'start', 'end', 'location')
    list_filter = ('start', 'end', 'location')
    search_fields = ('title', 'title2', 'location__name', 'description')

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
        if not change:
            try:
                lector = Lector.objects.get(user=request.user)
                obj.lector.add(lector)
            except Lector.DoesNotExist:
                pass

    def display_lectors(self, obj):
        return ", ".join([f"{lector.firstName} {lector.lastName or ''}" for lector in obj.lector.all()])
    display_lectors.short_description = 'Lectors'

@admin.action(description='Kopírovat vybrané položky')
def duplicate_workshops(modeladmin, request, queryset):
    for obj in queryset:
        obj.id = None  # Reset the primary key to duplicate
        obj.save()

class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'location', 'render_actions')
    actions = [duplicate_workshops]  # Keep this as a list of actions

    def render_actions(self, obj):  # Rename this method
        return format_html(
            '<a class="button" href="{}">Kopírovat</a>',
            f"/admin/danceapp/workshop/{obj.id}/change/",
        )
    render_actions.short_description = 'Actions'  # Set the column name in the admin list
    
admin.site.register(Workshop, WorkshopAdmin)

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



