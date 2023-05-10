/* Search functionality */

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

function viewPDF(url) {
  // Get the PDF file
  fetch(url)
    .then((response) => response.arrayBuffer())
    .then((data) => {
      // Load the PDF using pdf.js
      pdfjsLib.getDocument({ data: data }).promise.then((pdf) => {
        // Get the first page of the PDF
        pdf.getPage(1).then((page) => {
          // Set up the canvas element to display the page
          const canvas = document.getElementById("pdf-canvas");
          const context = canvas.getContext("2d");
          const viewport = page.getViewport({ scale: 1.5 });
          canvas.width = viewport.width;
          canvas.height = viewport.height;
          // Render the page onto the canvas
          page.render({ canvasContext: context, viewport: viewport });
          // Show the modal containing the canvas element
          const modal = document.getElementById("pdf-modal");
          modal.style.display = "block";
        });
      });
    });
}
function closePDF() {
  const modal = document.getElementById("pdf-modal");
  modal.style.display = "none";
}
