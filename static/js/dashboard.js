/* Dashboard Functionality */

// TOGGLE SIDEBAR
const menuBar = document.querySelector("#content nav .fa-solid.fa-bars");
const sidebar = document.getElementById("sidebar");

menuBar.addEventListener("click", function () {
  sidebar.classList.toggle("hide");
});

const switchMode = document.getElementById("switch-mode");

switchMode.addEventListener("change", function () {
  if (this.checked) {
    document.body.classList.add("dark");
  } else {
    document.body.classList.remove("dark");
  }
});

const form = document.getElementById("myForm");

// add event listener to form submit event
form.addEventListener('submit', function(event) {
  // prevent form from submitting
  event.preventDefault();

  // show the modal
  const modal = document.getElementById('myModal');
  // get the submit button inside the modal
  const submitBtn = document.getElementById('submitBtn');

  // add event listener to the submit button
  submitBtn.addEventListener('click', function() {
    // submit the form
    form.submit();
  });

});
