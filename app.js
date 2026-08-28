button = document.querySelector("#submit-btn");

button.addEventListener("click", async (event) => {
  event.preventDefault();

  textarea = document.getElementById("textarea1").value;
  results = document.getElementById("results");

  if (textarea.trim().length === 0) {
    results.textContent = "Please enter some tasks first";
    return;
  }

  button.disabled = true;
  button.textContent = "Processing...";

  try {
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

    const response2 = await fetch("http://127.0.0.1:5001/prioritize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ tasks: info }),
    });
    const data2 = await response2.json();
    const info_objects = JSON.parse(data2.result);
    results.innerHTML = "";

    ul_element = document.createElement("ul");
    ul_element.className = "task-list";

    p_element = document.createElement("p");
    p_element.className = "summary";

    p_element.textContent = info_objects.summary;
    results.appendChild(p_element);

    div_element = document.createElement("div");
    div_element.className = "conflicts";
    p1_element = document.createElement("p");
    p1_element.textContent = "Conflicts";
    div_element.appendChild(p1_element);

    conflicts_ul = document.createElement("ul");

    info_objects.ordered_tasks.forEach((element) => {
      li_element = document.createElement("li");
      lookup_button = document.createElement("button");
      show_results = document.createElement("div");

      lookup_button.textContent = "Look Up";
      lookup_button.className = "lookup-btn";
      li_element.textContent = element;

      lookup_button.addEventListener("click", async (event) => {
        const response3 = await fetch("http://127.0.0.1:5001/search-context", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ task: element }),
        });
        const data3 = await response3.json();

        show_results.textContent = data3.title + ": " + data3.content;
      });

      ul_element.appendChild(li_element);
      li_element.appendChild(lookup_button);
      li_element.appendChild(show_results);
    });
    results.appendChild(ul_element);

    if (info_objects.conflicts.length > 0) {
      info_objects.conflicts.forEach((element) => {
        list = document.createElement("li");
        list.textContent = element;
        conflicts_ul.appendChild(list);
      });

      div_element.appendChild(conflicts_ul);
      results.appendChild(div_element);
    }
  } catch (error) {
    results.textContent = "Something went wrong. Please try again.";
    console.log(error);
  } finally {
    button.textContent = "Submit";
    button.disabled = false;
  }
});
