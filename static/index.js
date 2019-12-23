$(function() {
    $('form').submit(function(e){
        e.preventDefault(); 
        var form = $(this);
        var data = {            
            'feedback': $("textarea[name='feedback']", form).val()
        };

        $.ajax({
            url: form.attr('action'),          
            data: data,
            type: 'POST',
            dataType: 'json',
            success: function(response) {
                if(response.res == 1 ){
                    $(".js-thank-you-positive", form).show();
                    $(".js-thank-you-negative", form).hide();
                }
                else{
                    $(".js-thank-you-positive", form).hide();
                    $(".js-thank-you-negative", form).show();
                };
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
   });
});