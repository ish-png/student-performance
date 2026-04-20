let history = [];

function switchTab(tab){
  document.querySelectorAll(".tab").forEach(t=>t.classList.remove("active"));
  document.getElementById(tab).classList.add("active");
}

async function predict(){

  const payload = {
    gender: gender.value,
    ethnicity: ethnicity.value,
    parental_education: education.value,
    lunch: lunch.value,
    test_prep: prep.value
  };

  const res = await fetch("/predict", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify(payload)
  });

  const data = await res.json();

  const resultBox = document.getElementById("result");

  resultBox.className = data.prediction === 1 ? "pass" : "fail";

  resultBox.innerHTML = `
    <h2>${data.result}</h2>
    <p>${data.message}</p>
    <strong>${data.probability}% Confidence</strong>
  `;

  updateTeacher(data);
}

function updateTeacher(data){
  history.push(data.result);

  document.getElementById("history").innerHTML =
    history.map(h=>`<li>${h}</li>`).join("");

  document.getElementById("alerts").innerHTML =
    data.prediction===0 ? "Student requires attention" : "All students performing well";
}