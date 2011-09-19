/**
 * Created by PyCharm.
 * User: chapson
 * Date: 17.09.11
 * Time: 20:35
 * To change this template use File | Settings | File Templates.
 */
jQuery(function() {
    $('.block-item_add_to_cart').each(function() {
        var _this = jQuery(this),
            params = _this.attr('onclick')(),
            form = $('form', this),
            quantity = params.quantity || 0;
        var url = form.attr('action'),
            label = $('input[type=submit]', form).attr("value");
        var anchor = $("<a href=\""+url+"\">"+label+"<span></span></a>")
        _this.updateQuantity = function(quantity){
            console.log(quantity);
            var text = '';
            if (quantity > 0){
                text = ' ('+quantity+')'
            }
            $('span', anchor).text(text);
        }
        $('.block-item_add_to_cart__link',this).append(anchor);
        form.hide();
        anchor.click(function(){
            $.ajax({url: url, data: form.serialize(),
                dataType: 'json',
                type: "post",
                success: function(data){
//                    console.log(data);
//                    $('span', anchor).text(' ('+data.show_quantity+')');
                    _this.updateQuantity(data.show_quantity);
                    if(simpleCart){ simpleCart.update(data); }
                    flash.show(data.message)
                },
                error: function(data){
                    flash.error(data.message || "error");
                }
                });
            return false;
        })
        _this.updateQuantity(quantity);
    });
});