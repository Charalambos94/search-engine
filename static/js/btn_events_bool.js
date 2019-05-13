$(function() {
    $('#search_boolean_btn').click(function() {

        $.ajax({
            url: 'btn_events_bool',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
