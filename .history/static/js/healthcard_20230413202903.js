
    const healthcard=document.getElementById('back-img');
    const hcname=document.getElementById('name');
    hcname.innerHTML=healthcard.src.substring(40,43);
    hcname.innerText="Hello";
    console.log(healthcard.src);

