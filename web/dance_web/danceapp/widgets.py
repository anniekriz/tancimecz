from django.contrib.admin.widgets import AdminTimeWidget

class CustomTimeWidget(AdminTimeWidget):
    class Media:
        js = (
            'admin/js/core.js',
            'admin/js/admin/RelatedObjectLookup.js',
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/jquery.init.js',
            'admin/js/actions.js',
            'static/js/custom_time_widget.js',  
        )

    def __init__(self, attrs=None, format=None):
        super().__init__(attrs, format)
        if attrs is None:
            attrs = {}
        attrs['class'] = 'vTimeField'
        attrs['data-error-msg'] = 'Zadejte čas ve formátu 18, 18:00 nebo 18:00:00.'
        self.attrs.update(attrs)