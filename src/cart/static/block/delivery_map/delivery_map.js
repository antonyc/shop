jQuery(function(){
    $('.block-delivery_map').each(function(){
        var _this = jQuery(this),
            params = _this.attr('onclick')(),
            map = $('.block-delivery_map__map div', this),
            address = $('.block-delivery_map__text', this);
        var map_visible = params.map_visible || false;
        _this._doAnimateMap = function(show){
            show ? map.show() : map.hide();
        }
        setTimeout(function(){ _this._doAnimateMap(map_visible); }, 1000)
        address.click(function(){
            map_visible = !map_visible;
            _this._doAnimateMap(map_visible);
        })
    })
})