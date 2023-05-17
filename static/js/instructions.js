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

  function updatecost() {
    var uploadText = document.querySelector(".upload");
    if (uploadText) {
      console.log(uploadText.value);
      var target = document.querySelector("#cost");
      if (target) {
        target.textContent=uploadText.value
      } else {
        console.error("Element with ID 'cost' not found.");
      }
    } else {
      console.error("Element with class 'update' not found.");
    }
  }