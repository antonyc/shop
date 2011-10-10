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
            quantity = params.quantity || 0,
            quantity_block = $('.block-simple_cart__quantity', this);
        _this.updateCart = function(data) {
            if (price_block) {
                price = data.total_price;
                price_block.text(price);
            };
            if (quantity_block && data.cart && data.cart.items) {
                var quantity = 0, length = data.cart.items.length;
                for(var i=0;i<length;i++){
                    quantity += data.cart.items[i].quantity
                };
                quantity_block.text(quantity)
            };
        };
        simpleCart.subscribe(_this);
    });
});