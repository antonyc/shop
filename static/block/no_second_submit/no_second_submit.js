jQuery(function() {

    $('.block-no_second_submit').each(function() {
        var _this = jQuery(this);
        $('form', this).submit(function(){
            var handler = function(){
                var submit = $('input[type=submit]', this);
                submit.attr('disabled', 'disabled');
                $('.spinner', _this).show();
            }
            setTimeout(handler, 1000)
        })
    })
});