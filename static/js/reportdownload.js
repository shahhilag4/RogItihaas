function downloadPDF(url) {
    const link = document.createElement("a");
    link.href = url;
    link.target = "_blank";
    link.download = "document.pdf"; // Specify the filename for the downloaded file
    
    // Programmatically trigger the download action
    link.click();
  }
  