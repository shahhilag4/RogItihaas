
const healthcard=document.getElementById('back-img');
const hcname=document.getElementById('name');
hcname.innerHTML=healthcard.src.substring(111,114);
console.log(healthcard.src);