document.addEventListener("DOMContentLoaded", function() {
  var rows = document.querySelectorAll("tbody tr");
  console.log(rows.length); // 打印表格行数量
  rows.forEach(function(row) {
    row.addEventListener("click", onTableRowClick);
  });

  var markers = [];
  var polyline;
//  var locations = {{ locations|tojson }};
//  var locations = JSON.parse('{{ locations|tojson|safe }}');
  var map = new AMap.Map('map', {
    resizeEnable: true,
    zoom: 13,
    center: [116.397428, 39.90923]
  });
  console.log(map);


  function addMarker(location) {
      console.log('hhhqqq');
      console.log(location);

    var marker = new AMap.Marker({
      position: [location.lng, location.lat],
      map: map
    });
    console.log(marker);
    markers.push(marker);
    console.log(markers);
  }

  function setPolyline(points) {
    if (polyline) {
      polyline.setMap(null);
    }
    polyline = new AMap.Polyline({
      path: points,
      isOutline: true,
      outlineColor: '#ffeeee',
      borderWeight: 2,
      strokeWeight: 5,
      strokeColor: '#0091ff',
      lineJoin: 'round'
    });
    polyline.setMap(map);
    console.log(polyline);
    map.setFitView(polyline);
  }

//  function clearMarkers() {
//  console.log(markers)
//    markers.forEach(function(marker) {
//      marker.setMap(null);
//    });
//    markers = [];
//  }

  function onTableRowClick(event) {
    console.log('Clicked row:', event.target);

    var row = event.target.closest('tr');
    var id = row.dataset.id;
    console.log(row)
    console.log(id); // 添加此语句
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          var location = JSON.parse(xhr.responseText);
          console.log(location);

          location.forEach(function(loc) {
            addMarker(loc);
            setPolyline([[loc.lng, loc.lat]]);
          });
        } else {
          console.log("XHR request failed: " + xhr.status);
        }
      }
    };
    xhr.open("GET", "/locations/" + id);
    xhr.send();
  }


  var map = new AMap.Map('map', {
    zoom: 12
});

});
