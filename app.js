button = document.querySelector("#Button1");

button.addEventListener("click", (event) => {
  textarea = document.getElementById("textarea1").value;
  results = document.getElementById("results");

  alert(textarea);

  fetch("http://127.0.0.1:5500/triage", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: textarea }),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      const tasks = JSON.parse(data.result);
      results.innerHTML = "";

      tasks.forEach((element) => {
        newList = document.createElement("li");
        newList.textContent = element;
        results.appendChild(newList);
      });
    });
});
