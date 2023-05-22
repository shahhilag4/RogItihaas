// Function to display the modal and populate the input field with existing instructions
function showModal() {
    $('#myModal').modal('show');
  }
  
  function saveInstructions() {
    var instructionInput = document.getElementById("instruction-input");
    var instructionsCell = document.getElementById("instructions-cell");
    instructionsCell.textContent = instructionInput.value;
    instructionsCell.style.width="100%"
    $('#myModal').modal('hide');
  }
  
  function closeModal() {
    $('#myModal').modal('hide');
  }