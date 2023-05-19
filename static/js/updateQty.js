const updateButtons = document.querySelectorAll(".status.success");

updateButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const quantityCell = button.parentNode.previousElementSibling;
	console.log(quantityCell);
    const quantityElement = quantityCell.querySelector(".quantity");
    
    if (!quantityCell || !quantityElement) {
      console.error("Unable to find quantity cell or quantity element.");
      return;
    }

    const originalContent = quantityElement.textContent;

    if (button.textContent === "Update") {
      const inputField = document.createElement("input");
      inputField.type = "text";
      inputField.className = "quantity";
      inputField.value = parseInt(originalContent);
      quantityCell.innerHTML = "";
      quantityCell.appendChild(inputField);
      button.textContent = "Save";
    } else {
      const inputField = quantityCell.querySelector(".quantity");
      
      if (!inputField) {
        console.error("Unable to find input field.");
        return;
      }
      
      const updatedQuantity = inputField.value;
      quantityCell.innerHTML = `<span class="quantity">${updatedQuantity}</span>`;
      button.textContent = "Update";
    }
  });
});
