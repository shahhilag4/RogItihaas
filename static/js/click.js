function searchDoc() {
	var input, tablebody, patientrow, patientuid, i, txtValue;
    input = document.getElementById("docname");
	filter = input.value;
    tablebody = document.getElementById("tableBody1");
    patientrow = tablebody.getElementsByTagName("tr");
    for (i = 0; i < patientrow.length; i++) {
        patientuid = patientrow[i].getElementsByClassName("drname")[0];
		txtValue = patientuid.textContent || patientuid.innerText;
        if (txtValue.indexOf(filter) > -1) {
            patientrow[i].style.display = "";
        } else {
            patientrow[i].style.display = "none";
        }
    }
}