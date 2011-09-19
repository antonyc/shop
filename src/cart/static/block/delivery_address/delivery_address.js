 jQuery(function(){
    var countriesCache = [],
        citiesCache = [],
        formPrefix = "address-",
		lastXhr;
    function processData(data){
        result = [];
        for(var i=0;i<data.length;i++){
            result[result.length] = {label: data[i].name, geonameid: data[i].geonameid};
        }
        return result
    }
    hidden_inputs = function(){
        var names = ['country', 'city']
        var result = {country: undefined, city: undefined}
        for(var i=0; i<names.length; i++){
            result[names[i]] = $("<input type=\"hidden\" name=\""+ formPrefix+names[i] +"\" />")
            $(this).append(result[names[i]])
        }
        return result
    }
    $('.block-delivery_address').each(function(){
        var _this = jQuery(this),
            params = _this.attr('onclick')();
        var country_text = $('input[name=%country__text]'.replace('%', formPrefix), this),
            city_text = $('input[name=%city__text]'.replace('%', formPrefix), this),
            country = $('input[name=%country]'.replace('%', formPrefix), this),
            city = $('input[name=%city]'.replace('%', formPrefix), this);
        $(country_text).autocomplete({
			minLength: 2,
			source: function( request, response ) {
				var term = request.term.toLowerCase();
				if ( term in countriesCache  ) {
					response( processData(countriesCache[term]) );
					return;
				}

				lastXhr = $.getJSON( "/geocoding/resolve/country/", request, function( data, status, xhr ) {
                    countriesCache [ term ] = data.countries;
					if ( xhr === lastXhr ) {
						response( processData(data.countries) );
					}
				});
			},
            select: function(country){
                return function(event, ui){
                    country.val(ui.item.geonameid);
                }
            }(country)

		});
        $(city_text).autocomplete({
			minLength: 1,
			source: function( request, response ) {
                var countryId = country.val();
                if (!countryId) { return }
                var term = request.term.toLowerCase();
                if ( term+countryId in citiesCache  ) {
                    response( processData(citiesCache[term+countryId]) );
                    return;
                }
                var url = "/geocoding/resolve/country/"+countryId+"/city/"
				lastXhr = $.getJSON( url, request, function( data, status, xhr ) {
                    citiesCache [ term+countryId ] = data.cities;
					if ( xhr === lastXhr ) {
						response( processData(data.cities) );
					}
				});
			},
            select: function(city){
                return function(event, ui){
                    city.val(ui.item.geonameid);
                }
            }(city)

		});
    })
})