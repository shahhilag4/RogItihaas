function saveDivAsPdf() {
    const element = document.getElementById('orderbill');
    const width = element.scrollWidth;
    const height = element.scrollHeight; // use scrollHeight to get full content height
    const pdf = new jsPDF('p', 'pt', [width, height]);
    const canvas = document.createElement('canvas');
    canvas.width = width*2;
    canvas.height = height*2;
    const context = canvas.getContext('2d');
    context.scale(1, 1);
    const options = {
        scale: 1,
        canvas: canvas,
        logging: true,
        width: width,
        height: height,
        useCORS: true,
    };

    html2canvas(element, options).then((canvas) => {
        const imgData = canvas.toDataURL('image/jpeg', 1.0);
        const imgWidth = width;
        const imgHeight = height;
        const xPos = 0;
        const yPos = 0;
        pdf.addImage(imgData, 'JPEG', xPos, yPos, imgWidth, imgHeight);
        pdf.save('bill.pdf');
    }, (error) => {
        console.error('Error converting div to PDF:', error);
    });
}
