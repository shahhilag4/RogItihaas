/* Multiple search bubbles - The Pinterest Suggestion Model */

let searchBox = document.querySelector(".search-bar");
let options = document.querySelectorAll(".option");

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

searchBox.addEventListener(
  "keyup",
  debounce(function (event) {
    let searchText = event.target.value;
    // filter search results here
  }, 300)
);

options.forEach((option) => {
  option.addEventListener("click", function () {
    if (this.classList.contains("selected")) {
      this.classList.remove("selected");
    } else {
      this.classList.add("selected");
    }
  });
});

function myFunction() {
  var input, tablebody, patientrow, patientuid, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toLowerCase();
  tablebody = document.getElementById("options");
  patientrow = tablebody.getElementsByClassName("med");
  for (i = 0; i < patientrow.length; i++) {
    patientuid = patientrow[i];
    txtValue = patientuid.innerText.trim(); // Remove leading and trailing spaces
    txtValue=txtValue.toLowerCase();
    if (txtValue.indexOf(filter) > -1) {
      patientrow[i].style.display = "";
    } else {
      patientrow[i].style.display = "none";
    }
  }
}

function addRow() {
  // (B1) GET TABLE
  var table = document.getElementById("demoA");

  // (B2) INSERT ROW
  var row = table.insertRow();

  // (B3) INSERT CELLS
  var cell = row.insertCell();
  cell.innerHTML = `<td><input type="text" list="dr" placeholder="Enter Medicine" />
  <datalist id="dr">
      <option value="Objective C">Objective C</option>
      <option value="C++">C++</option>
      <option value="C#">C#</option>
      <option value="Cobol">Cobol</option>
      <option value="Go">Go</option>
      <option value="Java">Java</option>
      <option value="JavaScript">JavaScript</option>
      <option value="Python">Python</option>
      <option value="PHP">PHP</option>
      <option value="Pascal">Pascal</option>
      <option value="Perl">Perl</option>
      <option value="R">R</option>
      <option value="Swift">Swift</option>
  </datalist>
</td>`;
  cell = row.insertCell();
  cell.innerHTML = `<input type="number" name="" placeholder="1" class="formInput inputValue"> mg`;
  cell = row.insertCell();
  cell.innerHTML = `<input type="number" name="" placeholder="1" class="formInput inputValue"> daily`;
  cell = row.insertCell();
  cell.innerHTML = `<input type="number" name="" placeholder="7" class="formInput inputValue"> days`;
  cell = row.insertCell();
  cell.innerHTML = `<input type="text" name="" placeholder="Take with food"
  class="formInput inputValue">`;
}
