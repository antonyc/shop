jQuery(function(){
    if(!YMaps) {console.log('Yandex Maps are not available'); return;}
    var MapPoint = function (geoPoint, editable) {
        var map, _this = this,
            offset = new YMaps.Point(-10, -29);
        _this.geoPoint = geoPoint;
        // Вызывается при добавления метки на карту
        this.onAddToMap = function (pMap, parentContainer) {
            map = pMap;

            getElement().appendTo(parentContainer);

            this.onMapUpdate();
        };
        // Вызывается при удаление метки с карты
        this.onRemoveFromMap = function () {
            if (getElement().parent()) {
                getElement().remove();
            }
        };
        // Вызывается при обновлении карты
        this.onMapUpdate = function () {
            // Смена позиции оверлея
            var position = map.converter.coordinatesToMapPixels(_this.geoPoint).moveBy(offset);

            getElement().css({
                left : position.x,
                top :  position.y,
                position: 'absolute'
            });
        };
        this.openBalloon = function() {};
        function getElement(){
            var element = $("<div class=\"block-delivery_map__point\"><img src=\"http://static.amadika.ru/media/i/unknown.png\" alt=\"\" /></div>");
            // Устанавливает z-index (такой же, как у метки)
            element.css("z-index", YMaps.ZIndex.Overlay);
            return (getElement = function(){
                return element;
            })();
        }
        this.toString = function(){ return 'MapPoint ' + getElement(); }
        return this;
    };
    var placeOnMap = function(map, Event, geoPoint, container, editable){
        if(map.alreadyHasMyPoint) {
            return map.alreadyHasMyPoint;
        }
        container._hasPoint = true;

        var placemark = new YMaps.Placemark(geoPoint, {hideIcon: true, draggable: container.editable});  //placeOnMap(mEvent.getGeoPoint());
        if(container.editable){
            container.input_lon.val(geoPoint.getLng());
            container.input_lat.val(geoPoint.getLat());
        }
        YMaps.Events.observe(placemark, placemark.Events.DragEnd, function (obj) {
            var current = obj.getGeoPoint().copy();
            container.input_lon.val(current.getLng());
            container.input_lat.val(current.getLat());
        });
        placemark.openBalloon = function(){
            if(!editable) return;
            var _placemark = this;
            map.openBalloon(placemark.getGeoPoint(), '<div class="block-delivery_map__baloon block-delivery_map__baloon_not_inited"><span class="block-mocklink">delete?</a<</div>');
            $('div.block-delivery_map__baloon_not_inited').each(function(){
                $(this).removeClass('block-delivery_map__baloon_not_inited');
                $('span', this).click(function(){
                    map.removeOverlay(placemark);
                    map.closeBalloon();
                    container.input_lon.val('');
                    container.input_lat.val('');
                })
            })
        };
        if(container.editable){
            placemark.setIconContent('Drag or click to delete')
        }
        map.addOverlay(placemark);
        map.alreadyHasMyPoint = geoPoint;
        return map.alreadyHasMyPoint;
    }
    $('.block-delivery_map__map').each(function(){

    });
    $('.block-delivery_map').each(function(){

        var _this = jQuery(this),
            params = _this.attr('onclick')(),
            map_block = $('.block-delivery_map__map div', this),
            address = $('.block-delivery_map__text', this),
            editable = params.editable || false,
            mapIsActive = false,
            map;
        _this.editable = editable;
        var map_visible = params.map_visible || false;
        var point = {lat: params.lat, lon: params.lon},
            _hasPoint = (point.lat != undefined) && (point.lon != undefined);
        _this._doAnimateMap = function(show){
            if(show) {
                map_block.show();
                _this.initializeMap();
            } else {
                map_block.hide();
            }
        }
        address.click(function(){
            map_visible = !map_visible;
            _this._doAnimateMap(map_visible);
            return false;
        });
        _this.initializeMap = function(){
            if(mapIsActive) return;
            map_block.css('height', '400px');
            map = new YMaps.Map($('div', this)[0]);
            map.addControl(new YMaps.Zoom());
            map.addControl(new YMaps.ScaleLine());
            var center = _hasPoint ? new YMaps.GeoPoint(point.lon, point.lat) : new YMaps.GeoPoint(37.64, 55.76);//DC: moscow
            var zoom = 15;
            map.setCenter(center, zoom);
            if(editable){
                var mapClickReaction = function(container){
                    return function(map, mEvent){
                        return placeOnMap(map, mEvent, mEvent.getGeoPoint(), container, editable)
                    }
                }(_this);
                _this.prepareInputs(_hasPoint ? point : null);
                YMaps.Events.observe(map, map.Events.Click, mapClickReaction);
            }
            if(_hasPoint){
                placeOnMap(map, null, new YMaps.GeoPoint(point.lon, point.lat), _this, editable);
            }
            mapIsActive = true;
        };
        _this.prepareInputs = function(point){
            _this.input_lon = $('<input type="hidden" name="address-lon" />');
            _this.input_lat = $('<input type="hidden" name="address-lat" />');
            _this.append(_this.input_lon);
            _this.append(_this.input_lat);
            if(point != null){
                _this.input_lon.val(point.lon);
                _this.input_lat.val(point.lat);
            };
        };
    });
});