
    const healthcard=document.getElementById('back-img');
    console.log(healthcard.src);
    const hcname=document.getElementById('name');
    hcname.innerHTML=healthcard.src.substring(40,43);
    hcname.innerHTML="Hello";

