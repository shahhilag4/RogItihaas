/* Submitting prescription functionality */

function submitPrescription() {
  const patientName = document.getElementById("patient-name").value;
  const medicationName = document.getElementById("medication-name").value;
  const dosage = document.getElementById("dosage").value;
  const frequency = document.getElementById("frequency").value;
  const duration = document.getElementById("duration").value;
  const instructions = document.getElementById("instructions").value;

  // Send prescription data to server
  // (Example code, replace with your own implementation)
  fetch("/submit-prescription", {
    method: "POST",
    body: JSON.stringify({
      patientName,
      medicationName,
      dosage,
      frequency,
      duration,
      instructions,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      alert("Prescription submitted successfully!");
    })
    .catch((error) => {
      alert("Error submitting prescription.");
    });
}
