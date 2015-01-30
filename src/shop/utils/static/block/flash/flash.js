//=== FLASH
flash = new function() {
    var defaultTimeout = 5000, maxMessages = 4;
    this._render = function(message, timeout, type) {
        timeout = timeout ? timeout : defaultTimeout;
        var _class = type || '';
        var list = jQuery('.am-flash .am-flash__list');
        if($('li', list).length == maxMessages){
            $($('li', list)[0]).remove();
        }
        var m = jQuery('<li class="' + _class + '">' + message + '</li>');
        list.append(m);
        setTimeout(function() {
            jQuery(m).fadeOut();
        }, timeout);
    }
    this.show = function(message, timeout) {
        this._render(message, timeout);
    }
    this.error = function(message, timeout) {
        this._render(message, timeout, 'error');
    }
};

jQuery('.am-flash').mouseover(function(){
    jQuery('li', this).fadeOut();
});