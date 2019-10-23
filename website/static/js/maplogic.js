// Creating map object
var myMap = L.map("map", {
  center: [33.7490, -84.3880],
  zoom: 9,
});

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);



// Load in geojson data
var geoData = "../static/js/metroatlantaall.geojson";

var geojson;
var legend;

function buildmap(year, incomelevel, burdenlevel) {
  var choice = year + incomelevel + burdenlevel
  var legendtitle = year + " " + incomelevel + " " + burdenlevel
  //console.log(feature.properties[choice][0]);
  console.log(choice)
// Grab data with d3
d3.json(geoData, function(data) {
  console.log(choice)
  // Create a new choropleth layer
  geojson = L.choropleth(data, {

    // Define what  property in the features to use
    valueProperty: choice,
	  

    // Set color scale
    scale: ["#ffffb2", "#b10026"],

    // Number of breaks in step range
    steps: 10,

    // q for quartile, e for equidistant, k for k-means
    mode: "q",
    style: {
      // Border color
      color: "#fff",
      weight: 1,
      fillOpacity: 0.3
    },
   
    // Binding a pop-up to each layer NEED TO FIX POPUP
    onEachFeature: function(feature, layer) {
      layer.bindPopup(feature.properties.NAMELSAD + "<br>" + legendtitle + "<br>" +
        "" + ((feature.properties[choice]) * 100).toFixed(2) + '%');
    }
  }).addTo(myMap);



  // Set up the legend
  legend = L.control({ position: "bottomright" });
  legend.onAdd = function() {
    var div = L.DomUtil.create("div", "info legend");
    var limits = geojson.options.limits;
    var colors = geojson.options.colors;
    var labels = [];

    // Add min & max
    var legendInfo = "<h4>" + legendtitle + "</h4>" +
      "<div class=\"labels\">" +
        "<div class=\"min\">" + limits[0] + "</div>" +
        "<div class=\"max\">" + ((limits[limits.length - 1]) * 100).toFixed(2) + '%' + "</div>" +
      "</div>";
      
    div.innerHTML = legendInfo;

    limits.forEach(function(limit, index) {
      labels.push("<li style=\"background-color: " + colors[index] + "\"></li>");
    });

    div.innerHTML += "<ul>" + labels.join("") + "</ul>";
    return div;
  };

  // Adding legend to the map
  legend.addTo(myMap);

});

};




function init() {
  // Grab a reference to the dropdown select element
  //var choice = d3.select('input[name="choice"]:checked').node().value;
  var incomelevel = document.getElementById('selDataIncome').options[document.getElementById('selDataIncome').selectedIndex].value;
  var burdenlevel = document.getElementById('selDataBurden').options[document.getElementById('selDataBurden').selectedIndex].value;
  var year = document.getElementById('selDataYear').options[document.getElementById('selDataYear').selectedIndex].value;
  console.log(incomelevel)
  console.log(burdenlevel)
  console.log(year)
    // Use the first sample from the list to build the initial plots
    buildmap(year, incomelevel, burdenlevel);

}

function optionChanged(choice) {
  // Fetch new data each time a new sample is selected
  var incomelevel = document.getElementById('selDataIncome').options[document.getElementById('selDataIncome').selectedIndex].value;
  var burdenlevel = document.getElementById('selDataBurden').options[document.getElementById('selDataBurden').selectedIndex].value;
  var year = document.getElementById('selDataYear').options[document.getElementById('selDataYear').selectedIndex].value;
  //var text = $( "#selDataIncome option:selected" ).text();
  console.log(incomelevel)
  console.log(burdenlevel)
  console.log(year)
  //var year = document.getElementById('selDataIncome').options[document.getElementById('selDataYear').selectedIndex].value;
  //var burden = document.getElementById('selDataIncome').options[document.getElementById('selDataBurden').selectedIndex].value;

    geojson.clearLayers()
    d3.select(".legend").remove();

    //legend.clearLayers()
    // Creating map object
    
  
  buildmap(year, incomelevel, burdenlevel);
  
}

// Initialize the dashboard
init();