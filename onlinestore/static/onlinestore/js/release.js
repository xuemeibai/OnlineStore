var mark = [];
        var map
        function initMap(){
            var iPad = {lat: 40.451823, lng: -79.939305};
            var mapProp = {
                center:new google.maps.LatLng(40.443299,-79.950591),
                zoom:14,
                mapTypeId:google.maps.MapTypeId.ROADMAP
            };
            map=new google.maps.Map(document.getElementById("GoogleMap"), mapProp);

            if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position){
                var pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                
                var my_marker = new google.maps.Marker({
                    position: pos,
                    map: map,
                    label: 'You Are Here',
                    icon: '/static/onlinestore/marker.png'
                });
                map.setCenter(pos);
            }, 
            function() {
                handleLocationError(true, infoWindow, map.getCenter());
            });
            
            } 
            else {
                // Browser doesn't support Geolocation
                handleLocationError(false, infoWindow, map.getCenter());
            }

            // This event listener calls addMarker() when the map is clicked.
            google.maps.event.addListener(map, 'click', function(event) {
                addMarker(event.latLng);
            });

            // Create the search box and link it to the UI element.
            var input = document.getElementById('pac-input');
            var searchBox = new google.maps.places.SearchBox(input);
            map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

            // Bias the SearchBox results towards current map's viewport.
            map.addListener('bounds_changed', function() {
                searchBox.setBounds(map.getBounds());
            });

            var markers = [];
            // Listen for the event fired when the user selects a prediction and retrieve
            // more details for that place.
            searchBox.addListener('places_changed', function() {
                var places = searchBox.getPlaces(); 
                if (places.length == 0) {
                    return;
                }   
                // Clear out the old markers.
                markers.forEach(function(marker) {
                    marker.setMap(null);
                });
                markers = [];   
                // For each place, get the icon, name and location.
                var bounds = new google.maps.LatLngBounds();
                places.forEach(function(place) {
                    if (!place.geometry) {
                        console.log("Returned place contains no geometry");
                        return;
                    }
                    var icon = {
                        url: place.icon,
                        size: new google.maps.Size(71, 71),
                        origin: new google.maps.Point(0, 0),
                        anchor: new google.maps.Point(17, 34),
                        scaledSize: new google.maps.Size(25, 25)
                    };    
                    // Create a marker for each place.
                    markers.push(new google.maps.Marker({
                        map: map,
                        icon: icon,
                        title: place.name,
                        position: place.geometry.location
                    }));  
                    document.getElementById('id_lat').innerHTML = place.geometry.location.lat()
                    document.getElementById('id_lng').innerHTML = place.geometry.location.lng()
                    if (place.geometry.viewport) {
                        // Only geocodes have viewport.
                        bounds.union(place.geometry.viewport);
                    } else {
                        bounds.extend(place.geometry.location);
                    }
                });
                map.fitBounds(bounds);
            });
            }

        // Adds a marker to the map.
        function addMarker(location) {
            deleteMarkers()
            var marker = new google.maps.Marker({
                position: location,
                map: map
            });
            document.getElementById('id_lat').innerHTML = location.lat()
            document.getElementById('id_lng').innerHTML = location.lng()
            mark.push(marker);
            showMarkers()
        }

        function setMapOnAll(map) {
          for (var i = 0; i < mark.length; i++) {
            mark[i].setMap(map);
          }
        }

        // Removes the markers from the map, but keeps them ithe array.
        function clearMarkers() {
          setMapOnAll(null);
        }

        // Shows any markers currently in the array.
        function showMarkers() {
          setMapOnAll(map);
        }

        // Deletes all markers in the array by removinreferences to them.
        function deleteMarkers() {
          clearMarkers();
          mark = [];
        }