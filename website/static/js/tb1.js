window.tableau=window.tableau||{},function(){function n(n){for(var t,r,u=document.getElementsByTagName("script"),i=0;i<u.length;i++)if(t=u[i].src,t.search(n)>0&&(r=t.lastIndexOf("/"),r>=0))return t.substring(0,r+1);return""}function t(n){document.write('<script src="'+n+'"><\/script>')}window.tableau._apiLoaded||(window.tableau._apiLoaded=!0,t(n("tableau-2.min.js")+"tableau-2.3.0.min.js"))}();

function initViz() {
var containerDiv = document.getElementById("tb1");
 url = "http://public.tableau.com/views/RegionalSampleWorkbook/Storms";
var options = {
   width: 1000,//containerDiv.offsetWidth,
   height: 852,//containerDiv.offsetHeight,
   hideTabs: true,
   hideToolbar: true,
   onFirstInteractive: function () {
     workbook = viz.getWorkbook();
     activeSheet = workbook.getActiveSheet();
   }
 };
 viz = new tableau.Viz(tb1, url,options);
}
initViz();