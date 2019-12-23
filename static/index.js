$(function () {
    $('form').submit(function (e) {
        e.preventDefault();

        var form = $(this);
        var feedback = $("textarea[name='feedback']", form).val();
        
        if(!feedback) return;
        
        $.ajax({
            url: form.attr('action'),
            data: { "feedback": feedback },
            type: 'POST',
            dataType: 'json',
            success: function (response) {
                if (response.res == 1) {
                    $(".js-thank-you-positive", form).removeClass('hidden');
                    $(".js-thank-you-negative", form).addClass('hidden');
                }
                else {
                    $(".js-thank-you-positive", form).addClass('hidden');
                    $(".js-thank-you-negative", form).removeClass('hidden');
                };
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});