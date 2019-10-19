function initViz() {
    var containerDiv = document.getElementById("vizContainer"),
    url = "https://public.tableau.com/views/AAHAWebProject-Story2Only/Story2-Whereandhowbadisit?:retry=yes&:embed=y&:display_count=yes&:origin=viz_share_link";

    var viz = new tableau.Viz(containerDiv, url);
}