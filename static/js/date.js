/* Prescription Template Functionality */

const month = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
const d = new Date();
var vdate = d.getDate();
var vmonth = month[d.getMonth()];
var vyear = d.getFullYear();
document.getElementById("date").innerHTML = vdate + " " + vmonth + " " + vyear;

$(function () {
  $("#fileupload").change(function (event) {
    var x = URL.createObjectURL(event.target.files[0]);
    $("#upload-img").attr("src", x);
  });
});
