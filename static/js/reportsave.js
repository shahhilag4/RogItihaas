function downloadPDF(pdfURL) {
    var link = document.createElement('a');
    link.href = pdfURL;
    link.target = '_blank'; // Open the PDF in a new tab/window
  
    // Set a default filename for the saved PDF
    var fileName = 'document.pdf';
    link.download = fileName;
  
    // Simulate a click on the link to trigger the download
    link.click();
  }
  