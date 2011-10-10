jQuery(function(){
    function resolveUserPosition(callback){

        if(navigator && navigator.geolocation){
            navigator.geolocation.getCurrentPosition(
            function(position){
                callback(position);
                console.log('geolocation success');
            },
            function (error) {
                switch(error.code){
                    case error.PERMISSION_DENIED:
                        flash.show('Пожалуйста, разрешите доступ к вашему местоположению',5000);
                        setTimeout(resolveUserPosition);
                        break;
                    case error.POSITION_UNAVAILABLE:
                        console.log('position unavailable')
                    case error.TIMEOUT:
                        console.log('timeout error')
//                        flash.show('Не удалось определить ваше местоположение')
                        // silently fail
                        break;
                }
//                map.setCenter(center, zoom);
            },
            {
                enableHighAccuracy : true,     // Режим получения наиболее точных данных
                timeout : 4000,                // Максиальное время ожидания ответа (в миллисекундах)
                maximumAge : 20000               // Максимальное время жизни полученных данных
            }
        );
        }
    };
    $('.block-cart').each(function(){
        var _this = jQuery(this),
            params = _this.attr('onclick')(),
            address_form = $('.block-address_form', this);
        address_form.disable_all = function(){
            var form = $(this);
            $('input', form).attr('disabled', 'disabled');
            form.hide();
        };
        address_form.enable_all = function(){
            var form = $(this);
            $('input', form).removeAttr('disabled');
            form.show();
        };

        $('.block-delivery__with_no_address input[type=radio]', this).click(function(){
            address_form.enable_all();
        });
        $('.block-delivery__with_address input[type=radio]', this).click(function(){
            address_form.disable_all();
        });
        address_form.disable_all();
        this.getNearestPoint = function(position){
            $.ajax({url: '/orders/nearest_delivery/',
                data: {lon: position.coords.longitude, lat: position.coords.latitude},
                dataType: 'json',
                success: function(data){
                    var id = data.id;
                    var nearest = $('.block-delivery__with_address_'+id, _this);
                    nearest.addClass('block-delivery__nearest');
                }})
//            console.log('get nearest from', position.coords)
        };
        resolveUserPosition(this.getNearestPoint);
    });
});