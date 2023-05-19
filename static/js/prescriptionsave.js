function saveDivAsPdf() {
  event.preventDefault();
    const element = document.getElementById('orderbill');
    const width = element.scrollWidth*1.8;
    const height = element.scrollHeight*1.8;
    const pdf = new jsPDF('p', 'pt', [width, height]);

    pdf.html(element, {
      callback: function () {
        pdf.save('bill.pdf');
        document.getElementById("myForm").submit();
      },
    });
  }
