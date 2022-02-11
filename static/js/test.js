const button = document.getElementById("btn-submit");
const resultBox = document.getElementById("results-div");

const spinner = document.createElement("span");
spinner.classList.add("spinner-grow");
spinner.classList.add("spinner-grow-sm");
spinner.setAttribute("role", "status");
spinner.setAttribute("aria-hidden", true);



function toggleButtonState() {
  if (button.disabled) {
    button.disabled = false;
    button.removeChild(spinner);
    button.innerText = "Compute";
  } else {
    button.innerText = "Loading...";
    button.insertBefore(spinner, button.firstChild);
    button.disabled = true;
  }
}

function toggleResultBox(show = true) {
  if (show === true) {
    resultBox.style.display = "block";
  } else {
    resultBox.style.display = "none";
  }
}

function successResultBox() {
  resultBox.classList.remove("alert-danger");
  resultBox.classList.add("alert-success");
}

function failResultBox() {
  resultBox.classList.remove("alert-success");
  resultBox.classList.add("alert-danger");
}

function fillTextGenResult(modelOutput) {
  let outputString = modelOutput;
  resultBox.innerHTML = modelOutput;
}

async function submitForm(event) {
  event.preventDefault();

  //取 Input Value
  const city = document.getElementById("city").value;

  var select = document.getElementById('area');
  const area = select.options[select.selectedIndex].value;

  const total_area = document.getElementById("total_area").value;

  var select1 = document.getElementById('building_type');
  const building_type = select1.options[select1.selectedIndex].value;

  const total_floor = document.getElementById("total_floor").value;
  
  var select2 = document.getElementById('state');
  const state = select2.options[select2.selectedIndex].value;

  var select3 = document.getElementById('usage');
  const usage = select3.options[select3.selectedIndex].value;

  var select4 = document.getElementById('material');
  const material = select4.options[select4.selectedIndex].value;

  const building_age = document.getElementById("building_age").value;

  const building_room_num = document.getElementById("building_room_num").value;

  const building_hall_num = document.getElementById("building_hall_num").value;

  const building_bathroom_num = document.getElementById("building_bathroom_num").value;

  var select5 = document.getElementById('residential_guard');
  const residential_guard = select5.options[select5.selectedIndex].value;

  var select6 = document.getElementById('berth');
  const berth = select6.options[select6.selectedIndex].value;

  var select7 = document.getElementById('elevator');
  const elevator = select7.options[select7.selectedIndex].value;

  toggleButtonState();
  toggleResultBox(false);
  try {
    await fetch("/test", {
      method: "POST",
      body: JSON.stringify({ city, area,total_area,building_type,total_floor,state,usage,material,
        building_age,building_room_num,building_hall_num,building_bathroom_num,residential_guard,
        berth,elevator}),
      headers: new Headers({
        "Content-Type": "application/json; charset=UTF-8",
      }),
    })
      .then(async (response) => {
        if (!response.ok) {
          const errorDetail = JSON.stringify(await response.json());
          throw new Error(
            `Request failed for ${response.statusText} (${response.status}): ${errorDetail}`
          );
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        successResultBox();
        fillTextGenResult(data);
      });
  } catch (error) {
    console.error(error);
    failResultBox();
    resultBox.innerText = "error";
  } finally {
    toggleButtonState();
    toggleResultBox();
  }
}

button.addEventListener("click", submitForm, true);
