from django.contrib.admin.widgets import AdminTimeWidget

class CustomTimeWidget(AdminTimeWidget):
    class Media:
        js = (
            'admin/js/core.js',
            'admin/js/admin/RelatedObjectLookup.js',
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/jquery.init.js',
            'admin/js/actions.js',
            'static/js/custom_time_widget.js',  # Path to your custom JS file
        )

    def __init__(self, attrs=None, format=None, choices=None):
        super().__init__(attrs, format)
        self.attrs['class'] = 'vTimeField'

    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs, renderer)
