
const healthcard=document.getElementById('back-img');
const hcname=document.getElementById('name');
hcname.innerHTML=healthcard.src.substring(40,43);
console.log(healthcard.src);