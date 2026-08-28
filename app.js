button = document.querySelector("#Button1");

button.addEventListener("click", async (event) => {
  event.preventDefault();

  textarea = document.getElementById("textarea1").value;
  results = document.getElementById("results");

  alert(textarea);

  const response = await fetch("http://127.0.0.1:5001/triage", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: textarea }),
  });
  const data = await response.json();
  const tasks = JSON.parse(data.result);
  results.innerHTML = "";

  tasks.forEach((element) => {
    newList = document.createElement("li");
    newList.textContent = element;
    results.appendChild(newList);
  });

  const response1 = await fetch("http://127.0.0.1:5001/classify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ tasks: tasks }),
  });
  const data1 = await response1.json();
  const info = JSON.parse(data1.result);
  results.innerHTML = "";

  info.forEach((element) => {
    newInfo = document.createElement("li");
    newInfo.textContent = `${element.task} - ${element.urgency} - ${element.category}`;
    results.appendChild(newInfo);
  });
});
