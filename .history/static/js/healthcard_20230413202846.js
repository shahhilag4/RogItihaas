
    const healthcard=document.getElementById('back-img');
    const hcname=document.getElementById('name');
    hcname.innerText=healthcard.src.substring(40,43);
    hcname.innerHTML="Hello";
    console.log(healthcard.src);

