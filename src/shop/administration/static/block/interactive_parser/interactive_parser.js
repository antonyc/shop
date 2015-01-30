jQuery(function() {

    $('.block-interactive_parser').each(function() {
        var _this = jQuery(this),
            params = _this.attr('onclick')();
        var timeoutHandler;
        var result = $("<div class=\"block-interactive_parser__result\"></div>");
        var parseText = function(){
            if(timeoutHandler){ clearTimeout(timeoutHandler) }
            var toParse = $(this);
            var handler = function(){
                result.text('<img src="%img%" alt="" />'.replace('%img%', params.url))
                $.ajax({url: params.url,
                    dataType: 'html',
                    data: 'text='+encodeURIComponent(toParse.val()),
                    success: function(data){
                        result.html(data)
                    },
                    error: function(){ result.text('') }
                })
            }
            result.text()
            timeoutHandler = setTimeout(handler, params.timeout || 1000);

        }
        _this.delegate('.block-interactive_parser__parse', 'keyup', parseText);
        _this.append(result);
        $('.block-interactive_parser__parse', this).each(function(){
            parseText.apply(this)
        })
    })
});