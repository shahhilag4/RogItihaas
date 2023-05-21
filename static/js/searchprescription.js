/* Prescription Searching functionality */

function myFunction() {
  var input, tablebody, patientrow, patientuid, i, txtValue, hideele;
  input = document.getElementById("myInput");
  filter = input.value.toLowerCase();
  tablebody = document.getElementById("mainContainer");
  console.log(tablebody);
  hideele = tablebody.getElementsByClassName("card");
  patientrow = tablebody.getElementsByTagName("h3");
  for (i = 0; i < patientrow.length; i++) {
    patientuid = patientrow[i];
    console.log(patientuid);
    txtValue = patientuid.textContent || patientuid.innerText;
    txtValue = txtValue.toLowerCase();
    if (txtValue.indexOf(filter) > -1) {
      hideele[i].style.display = "";
    } else {
      hideele[i].style.display = "none";
    }
  }
}
