jQuery(function() {

    $('.block-no_second_submit').each(function() {
        var _this = jQuery(this);
        $('form', this).submit(function(){
            var submit = $('input[type=submit]', this);
            submit.attr('disabled', 'disabled');
            submit.blur();
            var handler = function(context){
                return function(){
                    console.log(10);
                    $('.block-spinner', context).show();
                }
            }(_this);
            setTimeout(handler, 1000)
        })
    })
});