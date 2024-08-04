(function($) {
    $(document).ready(function() {
        console.log("Custom time widget script loaded");

        // Load jQuery Timepicker if not already loaded
        if (!$.fn.timepicker) {
            var script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jquery-timepicker/1.13.18/jquery.timepicker.min.js';
            document.head.appendChild(script);

            var link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = 'https://cdnjs.cloudflare.com/ajax/libs/jquery-timepicker/1.13.18/jquery.timepicker.min.css';
            document.head.appendChild(link);

            script.onload = function() {
                initializeTimePickers();
            };
        } else {
            initializeTimePickers();
        }

        function initializeTimePickers() {
            var customTimes = [
                '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'
            ];

            $('.vTimeField').each(function() {
                var $input = $(this);
                $input.timepicker({
                    timeFormat: 'HH:mm',
                    interval: 60,
                    minTime: '00:00',
                    maxTime: '23:59',
                    defaultTime: 'now',
                    startTime: '00:00',
                    dynamic: false,
                    dropdown: true,
                    scrollbar: true,
                    zindex: 3500
                });

                var dropdown = $input.siblings('.ui-timepicker-wrapper');
                dropdown.empty();
                customTimes.forEach(function(time) {
                    dropdown.append('<li>' + time + '</li>');
                });

                dropdown.on('click', 'li', function() {
                    var time = $(this).text();
                    $input.val(time).trigger('change');
                });
            });
        }

        // Custom error message handling for time fields
        $('.vTimeField').on('input', function() {
            var $input = $(this);
            var errorElement = $input.next('.errorlist');
            if (errorElement.length > 0) {
                var errorMessage = errorElement.find('li');
                if (errorMessage.length > 0 && errorMessage.text().includes('Enter a valid time')) {
                    errorMessage.text('Zadejte čas ve formátu 18, 18:00 nebo 18:00:00');
                }
            }
        });
    });
})(django.jQuery);
