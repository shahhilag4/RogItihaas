/* Health card content fetching */

var healthcard = document.getElementById("back-img");
var hcname = document.getElementById("name");
hcname.innerHTML = healthcard.src.substring(40, 43);
