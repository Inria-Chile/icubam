function add_marker (obj, map) {
  const position = {lat: obj.lat, lng: obj.lng};

  var infowindow = new google.maps.InfoWindow({
    content: obj.popup,
    maxWidth: 200
  });

  var marker = new google.maps.Marker({
    position: position,
    map: map,
    title: obj.label
  });
  marker.addListener('click', function() {
    infowindow.open(map, marker);
  });
}

function plotMap(data) {
  let center = {lat: data[0].lat, lng: data[0].lng};
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: center
  });

  for (i = 0; i < data.length; i++) {
    add_marker(data[i], map)
  }
}