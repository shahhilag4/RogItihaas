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
const aadhaarDialog = document.getElementById('alert-button');

console.log(aadhaarDialog);

function updatePlaceholder() {
  if (radioButtons[0].checked) {
    aadhaarInput.placeholder = "Aadhaar Card Number of Father + DOB";
    exampleDiv.style.display = 'block';
    aadhaarDialog.style.display = 'block';
  } else {
    aadhaarInput.placeholder = "Aadhaar Card Number";
    exampleDiv.style.display = 'none';
    aadhaarDialog.style.display = 'none';
  }
}

radioButtons.forEach((radio) => {
  radio.addEventListener('change', updatePlaceholder);
});

const modal = document.getElementById("aadhaar-dialog");

function showAlert() {
  event.preventDefault();
  modal.style.display = "block";
}

function hideAlert() {
  modal.style.display = "none";
}

// select the form element
const form = document.querySelector('.sign-up-form');

// select the radio buttons
const withAadhaarRadio = document.querySelector('input[value="aadhaar_card"]');
const withoutAadhaarRadio = document.querySelector('input[value="no_aadhaar_card"]');

// add event listener to form submit event
form.addEventListener('submit', function(event) {
  // prevent form from submitting
  event.preventDefault();

  // get the input value and selected radio button value
  const aadhaarInput = document.querySelector('input[name="patientaadhar1"]');
  const selectedRadio = document.querySelector('input[name="patienttype"]:checked');

  // check if the selected radio is "Without aadhaar card"
  if (selectedRadio.value === 'no_aadhaar_card') {
    // validate the input using regex
    const regex = /^\d{20}$/;
    if (regex.test(aadhaarInput.value)) {
      // submit the form if validation passes
      form.submit();
    } else {
      // display error message if validation fails
      alert('Aadhaar card number should be 20 digits long.');
    }
  } else {
    // validate the input using regex
    const regex = /^\d{12}$/;
    if (regex.test(aadhaarInput.value)) {
      // submit the form if validation passes
      form.submit();
    } else {
      // display error message if validation fails
      alert('Aadhaar card number should be 12 digits long.');
    }
  }

});


