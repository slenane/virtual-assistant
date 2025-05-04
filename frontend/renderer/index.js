const submitButton = document.querySelector("#submit");
const input = document.querySelector("#input");
const greeting = document.querySelector("#greeting");

const initApp = async () => {
  const res = await fetch("http://localhost:5000/api/init", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  const data = await res.json();
  if (data.response) {
    greeting.innerHTML = data.response;
  }
};

const sendMessageToBackend = async (message) => {
  const res = await fetch("http://localhost:5000/api/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();
  console.log("Response from backend: ", data);
};

document.addEventListener("DOMContentLoaded", () => {
  initApp();
});

submitButton.addEventListener("click", () => {
  sendMessageToBackend(input.value);
});
