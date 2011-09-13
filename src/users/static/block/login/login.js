$(function(){
    $('.block-login').each(function(){
        var _this = jQuery(this),
        params = _this.attr('onclick')();
        var show = params.show || 'loginza';
        var straight = $('.login__straight', _this),
            loginza = $('.login__loginza', _this),
            start_straight = $('.login__start_straight', _this),
            start_loginza = $('.login__start_loginza', _this);
        straight.hide();
        var show_function = function(show){
            if(show == 'loginza'){
                loginza.show();
                start_straight.show();
                start_loginza.hide();
                straight.hide();
            } else {
                loginza.hide();
                start_straight.hide();
                start_loginza.show();
                console.log(start_loginza);
                straight.show();
            }
        }
        show_function(show);
        $('a', start_straight).click(function(){
            show_function('straight');
            return false;
        });
        $('a', start_loginza).click(function(){
            show_function('loginza');
            return false;

        });

    });
})