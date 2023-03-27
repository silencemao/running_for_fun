document.addEventListener("DOMContentLoaded", function() {
  // 声明变量使用 const
  const rows = document.querySelectorAll("tr");
  const buttons = document.querySelectorAll("#trackList button");
  const markers = [];
  let polyline;
  const map = new AMap.Map("map", {
    resizeEnable: true,
    zoom: 13,
    center: [116.397428, 39.90923]
  });

  // 统一封装添加标记 Marker 和连线 Polyline 的函数，减少代码重复
  function addMarker(location) {
    const marker = new AMap.Marker({
      position: [location.lng, location.lat],
      map: map
    });
    markers.push(marker);
  }

  function setPolyline(points) {
    if (polyline) {
      polyline.setMap(null);
    }

    polyline = new AMap.Polyline({
      path: points,
      isOutline: true,
      outlineColor: "#ffeeee",
      borderWeight: 2,
      strokeWeight: 5,
      strokeColor: "#0091ff",
      lineJoin: "round"
    });

    polyline.setMap(map);
    map.setFitView(polyline);
  }

  // 将代码封装成函数，传入需要的参数
  function getLocations(url) {
    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          const location = JSON.parse(xhr.responseText);

          location.forEach(function(loc) {
            addMarker(loc);
            setPolyline([[loc.lng, loc.lat]]);
          });
        } else {
          console.log("XHR request failed: " + xhr.status);
        }
      }
    };

    xhr.open("GET", url);
    xhr.send();
  }

  function getTrack(url, trackID) {
    const formData = new FormData();
    formData.append("track_id", trackID);
    const xhr = new XMLHttpRequest();

    xhr.open("POST", url);

    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          const data = JSON.parse(xhr.responseText);
          const path = data.map(function(t) {
            return [t.longitude, t.latitude];
          });

          map.clearMap();

          const polyline = new AMap.Polyline({
            path: path,
            strokeColor: "#3366FF",
            strokeWeight: 6,
            strokeOpacity: 1,
            strokeStyle: "solid",
            showDir: true
          });

          polyline.setMap(map);

          map.setFitView(polyline, { duration: 500 });
        } else {
          alert("Error: " + xhr.responseText);
        }
      }
    };

    xhr.send(formData);
  }

  // 使用事件委托，添加事件监听器
//  rows.addEventListener("click", function(event) {
//    const id = event.target.closest("tr").dataset.id;
//    console.log(id);
//    if (id) {
//      getLocations(`/locations/${id}`);
//    }
//  });

  rows.forEach(function(row) {
     row.addEventListener("click", function() {
        console.log(row);
        const rowID = row.getAttribute("data-id");
        console.log(rowID);
        if (rowID) {
            getTrack("/get_track1", rowID)
        }
     });
  });

  buttons.forEach(function(button) {
    button.addEventListener("click", function() {
      const trackID = button.getAttribute("data-track");

      if (trackID) {
        getTrack("/get_track", trackID);
      }
    });
  });

});
