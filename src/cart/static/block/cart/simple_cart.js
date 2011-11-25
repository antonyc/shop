var simpleCart = {};
simpleCart.update = function(data) {
    var l = this.subscribers.length;

    for (var i = 0; i < l; i++) {
        this.subscribers[i].updateCart(data);
    };
};
simpleCart.subscribers = [];
simpleCart.subscribe = function(subscriber) {
    this.subscribers[this.subscribers.length] = subscriber;
};

jQuery(function() {
    $('.block-simple_cart').each(function() {
        var _this = jQuery(this),
            params = _this.attr('onclick')(),
            price = params.price || 0,
            price_block = $('.block-simple_cart__price', this),
            quantity = params.items || 0,
            quantity_block = $('.block-simple_cart__quantity', this),
            empty_cart_block = $('.block-simple_cart__empty', this),
            filled_cart_block = $('.block-simple_cart__not_empty', this);
        _this.renderCart = function(visible){
            if(visible){
                filled_cart_block.show();
                empty_cart_block.hide();
            } else {
                filled_cart_block.hide();
                empty_cart_block.show();
            }
        }
        _this.renderCart(quantity > 0);
        _this.updateCart = function(data) {
            if (price_block) {
                price = data.total_price;
                price_block.text(price);
            };
            _this.renderCart(data.cart && data.cart.items && data.cart.items.length > 0);
            if (quantity_block && data.cart && data.cart.items) {
                var quantity = 0, length = data.cart.items.length;
                for(var i=0;i<length;i++){
                    quantity += data.cart.items[i].quantity
                };

                quantity_block.text(quantity + " " + data.count_items)
            };
        };
        simpleCart.subscribe(_this);
    });
});