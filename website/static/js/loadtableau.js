function initViz() {
  var containerDiv = document.getElementById("pie"),
  url = "https://public.tableau.com/views/CitiBikeSeniors/YoyTrendsStory";
  
  var viz = new tableau.Viz(pie, url);
}

initViz();