function saveDivAsPdf() {
  event.preventDefault();
  const element = document.getElementById('orderbill');
  const width = element.scrollWidth;
  const height = element.scrollHeight;

  html2canvas(element, { scale: 2 })
    .then((canvas) => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'pt', [width, height]);
      pdf.addImage(imgData, 'PNG', 0, 0, width, height);

      // Save the PDF
      pdf.save('bill.pdf');
      document.getElementById('myForm').submit();
    })
    .catch((error) => {
      console.error('Error rendering HTML to canvas:', error);
    });
}
