var x = document.getElementById("container-hide");
x.style.display = "none";

function myFunction() {
  var x = document.getElementById("container-hide");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}