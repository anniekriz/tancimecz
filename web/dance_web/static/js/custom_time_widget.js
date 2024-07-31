(function($) {
    $(document).ready(function() {
        var customTimes = [
            '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'
        ];

        // Add custom times to the clock button dropdown
        function addCustomTimes() {
            $('select.vTimeField').each(function() {
                var $select = $(this);
                if ($select.data('customized')) {
                    return;
                }

                $select.data('customized', true);
                $select.empty();
                customTimes.forEach(function(time) {
                    $select.append(new Option(time, time));
                });
            });
        }

        // Override the default time picker initialization
        $('.vTimeField').on('focus', function() {
            addCustomTimes();
        });

        // Ensure custom times are added when the document is loaded
        addCustomTimes();
    });
})(django.jQuery);