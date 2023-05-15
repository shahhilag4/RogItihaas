/* Signin and Signup Functionality */

const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});


const radioButtons = document.querySelectorAll('input[type="radio"]');
const aadhaarInput = document.querySelector('input[name="patientaadhar1"]');
const exampleDiv = document.getElementById('example');

function updatePlaceholder() {
  if (radioButtons[0].checked) {
    console.log(radioButtons[0].value);
    console.log(aadhaarInput.placeholder);
    aadhaarInput.placeholder = "Aadhaar Card Number of Father + DOB";
    exampleDiv.style.display = 'block';
  } else {
    console.log(radioButtons[1].value);
    aadhaarInput.placeholder = "Aadhaar Card Number";
    exampleDiv.style.display = 'none';
  }
}

radioButtons.forEach((radio) => {
  radio.addEventListener('change', updatePlaceholder);
  console.log(radio);
});

