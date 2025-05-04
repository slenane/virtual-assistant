console.log("INIT");

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

const submitButton = document.querySelector("#submit");
const input = document.querySelector("#input");

submitButton.addEventListener("click", () => {
  sendMessageToBackend(input.value);
});
