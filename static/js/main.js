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
  //(4) Update Count
  var countCell=document.getElementById("count");
  var count=parseInt(countCell.value);
  if(count>=1)
  {
    count=count+1;
    console.log(count);
    countCell.value=count;
  }
  // (B3) INSERT CELLS
  console.log(count);
  var cell = row.insertCell();
  cell.innerHTML = `<td><input type="text" list="dr" name="medicine${count}"
  placeholder="Enter Medicine" />
  <datalist id="dr">
  <option value="Paracetamol">Paracetamol</option>
  <option value="Citrazine">Citrazine</option>
  </datalist>
  </td>`;
  
  cell = row.insertCell();
  cell.innerHTML = `<td><input type="number" name="mg${count}" value="10" class="formInput inputValue"> mg
  </td>`;
  cell = row.insertCell();
  cell.innerHTML = `<td><input type="number" name="dose${count}" value="1" class="formInput inputValue">
  daily
  </td>`;
  cell = row.insertCell();
  cell.innerHTML = ` <td><input type="number" name="days${count}" value="3" class="formInput inputValue">
  days
  </td>`;
  cell = row.insertCell();
  cell.innerHTML = `<td><input type="text" name="food${count}" placeholder="Take with food"
  class="formInput inputValue"></td>`;
  
}

function deleteRow(){
  // (B1) GET TABLE
  var table = document.getElementById("demoA");
  var rowCount = table.rows.length-1; //Remove header
  // (B2) DELETE ROW
  if (rowCount > 1) { 
    table.deleteRow(rowCount);
  }
  var countCell=document.getElementById("count");
  var count=parseInt(countCell.value);
  if(count>1)
  {
    count=count-1;
    console.log(count);
    countCell.value=count;
  }
  // (3) Update Count
}

