const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
	event.preventDefault();

	const patientName = document.getElementById('patient_name').value;
	const patientAge = document.getElementById('patient_age').value;
	const consentText = document.getElementById('consent_text').value;

	console.log(`Patient Name: ${patientName}`);
	console.log(`Patient Age: ${patientAge}`);
	console.log(`Consent: ${consentText}`);

	form.reset();
});
