jQuery(function() {
    /* это блок отображающийся при оформлении заказа */
    function changeQuantity(params, quantity, callback) {
        /* просто сделать AJAX запрос с заданными параметрами */
        $.ajax({url: params.url,
            data: {quantity: quantity, csrfmiddlewaretoken: params.token},
            type: 'post',
            dataType: 'json',
            error: function(data) {
                flash.error(data.message);
            },
            success: callback
        });
    };

    $('.block-cart_item').each(function() {

        var _this = jQuery(this),
            params = _this.attr('onclick')(),
            i18n = params.i18n || {};
        var pendingQuantityChange, func;
        // setting + - buttons
        var input = $('.block-cart_item__quantity input', this);
        var minus = $('<span class="block-mocklink minus">-</span>'),
            plus = $('<span class="block-mocklink minus">+</span>');
//        input.attr('disabled', 'disabled');
        /* и минус и плюс создают отложенный вызов функции, которая делает AJAX
        * запрос изменяя количество товара в корзине*/
        minus.click(function() {
            var val = input.val() - 0;
            if (val < 2) { return }
                input.val(input.val() - 0 - 1);
                if (pendingQuantityChange) {
                    clearTimeout(pendingQuantityChange)

                }
                var func = function(params, quantity, callback) {
                    return function() {
                        changeQuantity(params, quantity, callback);
                    }
                }(params, input.val(), function(data) {
                    if(simpleCart){ simpleCart.update(data); }
                    input.val(data.show_quantity);
                })
                pendingQuantityChange = setTimeout(func, 1500);

        });
        plus.click(function() {
            input.val(input.val() - 0 + 1);
            if (pendingQuantityChange) {
                clearTimeout(pendingQuantityChange)
            }
            var func = function(params, quantity, callback) {
                return function() {
                    changeQuantity(params, quantity, callback);
                }
            }(params, input.val(), function(data) {
                if(simpleCart){ simpleCart.update(data); }
                input.val(data.show_quantity);
            })
            pendingQuantityChange = setTimeout(func, 1500);

        });
        $('.block-cart_item__quantity',_this).prepend(minus);
        $('.block-cart_item__quantity',_this).append(plus);

        // setting "delete" button
        var del = $('.block-cart_item__remove', this);
        var remove = $('<span class="block-mocklink">' + i18n.remove + '</a>');
        remove.click(function(){
            if(pendingQuantityChange) clearTimeout(pendingQuantityChange);
            $.ajax({url: params.url,
                data: {quantity: 0, csrfmiddlewaretoken: params.token},
                dataType: 'json',
                type: 'post',
                success: function(data){
                    _this.hide(1000);
                    remove = function(element, data){ return function(){ if(simpleCart){ simpleCart.update(data); }; element.remove(); } }(_this, data);
                    setTimeout(remove, 1001);
                },
                error: function(){
                    flash.error('Failed to remove')
                }
            });
        })
        del.append(remove);
    });
});