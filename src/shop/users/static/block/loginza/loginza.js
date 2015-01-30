$(function(){
    $('.b-get-loginza-data').each(function(){
        var _this = jQuery(this),
        params = _this.attr('onclick')();
        $.ajax({
            url: params.url,
            success: function(data){
                console.log(data);
            }
        });
    });
});