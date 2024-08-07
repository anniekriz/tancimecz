$(document).ready(function() {
    $('#search-input').on('keyup', function() {
        var query = $(this).val();
        $.ajax({
            url: $('#search-form').attr('action'),
            data: {
                'query': query
            },
            dataType: 'json',
            success: function(data) {
                $('#search-results').html(data.results_html);
            }
        });
    });
});