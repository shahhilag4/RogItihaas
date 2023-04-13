function myFunction() {
	var input, tablebody, patientrow, patientuid, i, txtValue;
    input = document.getElementById("myInput");
	filter = input.value;
    tablebody = document.getElementById("tableBody");
    patientrow = tablebody.getElementsByTagName("tr");
    for (i = 0; i < patientrow.length; i++) {
        patientuid = patientrow[i].getElementsByClassName("patientuid")[0];
		txtValue = patientuid.textContent || patientuid.innerText;
        if (txtValue.indexOf(filter) > -1) {
            patientrow[i].style.display = "";
        } else {
            patientrow[i].style.display = "none";
        }
    }
}