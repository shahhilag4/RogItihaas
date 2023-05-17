// Function to display the modal and populate the input field with existing instructions
function editInstructions() {
    var instructionsCell = document.getElementById("instructions-cell");
    var instructionInput = document.getElementById("instruction-input");
    instructionInput.value = instructionsCell.textContent;
    $('#myModal').modal('show');
  }
  
  function saveInstructions() {
    var instructionInput = document.getElementById("instruction-input");
    var instructionsCell = document.getElementById("instructions-cell");
    instructionsCell.textContent = instructionInput.value;
    $('#myModal').modal('hide');
  }
  