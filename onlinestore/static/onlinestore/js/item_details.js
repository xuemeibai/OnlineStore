var map
var my_pos

function initMap(){
    var CMU = new google.maps.LatLng(40.443299,-79.950591)
    var mapProp = {
        center: CMU,
        zoom: 13,
        mapTypeId:google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("GoogleMap"), mapProp);
    var infowindow = new google.maps.InfoWindow
    my_pos = CMU
    
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position){
        var my_pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        
        var my_marker = new google.maps.Marker({
            position: my_pos,
            map: map,
            label: 'You Are Here',
            icon: '/static/onlinestore/marker.png'
        });
        map.setCenter(my_pos);
        draw(my_pos);
    }, 
    function() {
        handleLocationError(true, infoWindow, map.getCenter());
    });
    
    } 
    else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
        draw(CMU);
    }
        
}

function draw(my_pos){
    var price = Number(document.getElementById("price").innerHTML)
    var lat_k = Number(document.getElementById("lat").innerHTML)
    var lng_k = Number(document.getElementById("lng").innerHTML)
    var img_k = document.getElementById("img").innerHTML
    var position = {lat: lat_k, lng:lng_k};

    var distance = get_distance(my_pos, position);
    //var distance = google.maps.geometry.spherical.computeDistanceBetween(my_pos,position);
    var contentString =
    '<div id="content">'+
        '<h3 id="firstHeading" class="firstHeading">'+ document.getElementById("name").innerHTML +'</h3>'+
        '<img src="/get_photo/'+img_k+'" width="100px">'+
        '<div>'+
            '<label>Price: $ '+price+'</label>'+'</div>'+
        '<div>'+
            '<label>Distance: '+distance+' km</label>'+'</div>'+
    '</div>'
    ;
    //{% url '+"'get_photo' "+img_k+' %}
    
    var marker = new google.maps.Marker({
        position: position,
        map: map,
        title: document.getElementById("name").innerHTML+'\xa0'+document.getElementById("condition").innerHTML
        });
    add_info(marker,contentString);      

}

function add_info(marker,contentString){
    var infowindow = new google.maps.InfoWindow({content: contentString});
    marker.addListener('click', function(){
        infowindow.open(map, marker);
    });
}

function get_distance(my_pos, position){
    var lat = [my_pos.lat, position.lat]
    var lng = [my_pos.lng, position.lng] //var R = 6371; // km (change this constant to get miles)
    var R = 6378137; // In meters
    var dLat = (lat[1] - lat[0]) * Math.PI / 180;
    var dLng = (lng[1] - lng[0]) * Math.PI / 180;
    var dLat1 = lat[0] * Math.PI / 180;
    var dLat2 = lat[1] * Math.PI / 180;
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(dLat1) * Math.cos(dLat1) * Math.sin(dLng / 2) * Math.sin(dLng / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var d = R * c;
    d = parseFloat(d)/1000
    return d.toFixed(2);
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.\n'+
                          'Your postition is set to CMU campus as default');
    infoWindow.open(map);
}
//google.maps.event.addDomListener(window, 'load', initMap);
//window.onload = draw_map;