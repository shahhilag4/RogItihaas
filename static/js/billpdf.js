function generatePDF() {
    const element = document.getElementById('orderbill');
    const width = element.scrollWidth;
    const height = element.scrollHeight;
  
    html2canvas(element, { scale: 2 })
      .then((canvas) => {
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'pt', [width, height]);
        pdf.addImage(imgData, 'PNG', 0, 0, width, height);
  
        // Save the PDF
        savePDF(pdf.output('blob'));
      })
      .catch((error) => {
        console.error('Error rendering HTML to canvas:', error);
      });
  }
  
  function savePDF(pdfData) {
    const formData = new FormData();
    formData.append('pdfData', pdfData, 'onlinebill.pdf');
  
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/generate_pdf');
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        // PDF saved successfully
        console.log('PDF saved successfully');
        // Redirect to /deliverytrack
        window.location.href = '/deliverytrack';
      }
    };
    xhr.send(formData);
  }
  