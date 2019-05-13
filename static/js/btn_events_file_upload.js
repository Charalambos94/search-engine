$(function() {
    $('#crawler_file_btn').click(function() {

        $.ajax({
            url: 'btn_events_file_upload',
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
