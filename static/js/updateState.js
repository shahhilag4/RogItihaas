const updateButton = document.getElementById("update-btn");
const statusCell = document.querySelector("td[data-label='Status']");

// Add event listener to "Update" button
updateButton.addEventListener("click", () => {
    if(statusCell.getAttribute("contenteditable")=="true")
    {
        statusCell.setAttribute("contenteditable", "false");
        statusCell.innerHTML = `
        <select name="status">
          <option value="accepted">Accepted</option>
          <option value="packing">Packing</option>
          <option value="on the way">On the Way</option>
          <option value="delivered">Delivered</option>
        </select>
      `;
        updateButton.style.display = "block";
    }
    else
    {
        const selectedValue = document.querySelector("select[name='status']").value;
        statusCell.textContent = selectedValue;
        statusCell.setAttribute("contenteditable", "true");
        updateButton.style.display = "block";
    }
});

// // Add event listener to updated status cell
// statusCell.addEventListener("click", () => {
// });
