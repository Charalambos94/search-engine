$(function() {
    $('#crawler_btn').click(function() {

        $.ajax({
            url: 'btn_events_crawler',
            data: $('form').serialize(),
            type: ['POST','GET'],
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
