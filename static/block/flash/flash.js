//=== FLASH
flash = new function() {
    var defaultTimeout = 5000;
    this._render = function(message, timeout, type) {
        timeout = timeout ? timeout : defaultTimeout;
        var _class = type || '';
        var m = jQuery('<li class="' + _class + '">' + message + '</li>');
        jQuery('.am-flash .am-flash__list').append(m);
        setTimeout(function() {
            jQuery(m).remove();
        }, timeout);
    }
    this.show = function(message, timeout) {
        this._render(message, timeout);
    }
    this.error = function(message, timeout) {
        this._render(message, timeout, 'error');
    }
};