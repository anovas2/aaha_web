



// Get new data whenever the dropdown selection changes
function getlatlon() {
    var resData;
    let address = document.getElementById('address_place').value;
    console.log(address);
    let url = '/address_data/' + address;
    console.log(url);
    d3.json(url, function (json) {
        console.log(json);
        resData = json;
        d3.select('#address_place').property('value', resData.address);

        d3.select('#burden_table').html(resData.burden_data_html);

        d3.select('#address').text(resData.address);
        d3.select('#af_rent').text(resData.af_rent);
        d3.select('#fmr').text(resData.fmr);
        d3.select('#lat').text(resData.lat);
        d3.select('#lon').text(resData.lon);
        d3.select('#geoid').text(resData.geoid);

        // var table = $('<table/>').html('<thead><tr><th>Property Feature</th><th>Details</th></tr></thead>').appendTo('#myTable'),
        //     tbody = table.append('<tbody/>');
        // $.each(resData, function (key, value) {
        //     tbody.append('<tr><td>' + key + '</td><td>' + value + '</td></tr>');
        // });
    chart_tool(resData.fmr,resData.af_rent)
    street_view(resData.lat,resData.lon)
    });
}
// // Plot the default route once the page loads
// var defaultURL = "/emoji_char";
// d3.json(defaultURL).then(function(data) {
//   var data = [data];
//   var layout = { margin: { t: 30, b: 100 } };
//   Plotly.plot("bar", data, layout);
// });
//
// // Update the plot with new data
// function updatePlotly(newdata) {
//   Plotly.restyle("bar", "x", [newdata.x]);
//   Plotly.restyle("bar", "y", [newdata.y]);
// }

// Get new data whenever the dropdown selection changes
function chart_tool(fmr,af_rent) {
  console.log(fmr,af_rent);
var data = [
  {
    domain: { x: [0, 1], y: [0, 1] },
    value: af_rent,
    title: { text: "Affordable Rent Vs Fair Market Rent" },
    type: "indicator",
    mode: "gauge+number+delta",
    delta: { reference: fmr },
    gauge: {
      axis: { range: [null, fmr] },
      steps: [
        { range: [0, af_rent], color: "lightgray" },
        { range: [af_rent, fmr], color: "red" }
      ],
      threshold: {
        line: { color: "red", width: 4 },
        thickness: 0.75,
        value: af_rent
      }
    }
  }
];

var layout = { width: 600, height: 450, margin: { t: 0, b: 0 } };
Plotly.newPlot("gd", data, layout);
}

function street_view(lat,lon) {

    console.log(lat,lon)
  var fenway = {lat: lat, lng: lon};
  var map = new google.maps.Map(document.getElementById('map2'), {
    center: fenway,
    zoom: 14
  });
  var panorama = new google.maps.StreetViewPanorama(
      document.getElementById('pano2'), {
        position: fenway,
        pov: {
          heading: 34,
          pitch: 10
        }
      });
  map.setStreetView(panorama);
}


