function handleInput() {
  const search_input = document.getElementById("search_input");
  console.log("clicked:", search_input.value);
  if(search_input.value.length == 0) {
    console.log("input is empty string");
    return;
  }
  let url = 'http://127.0.0.1:' + window.location.port + '/search/';
  url += search_input.value
  fetch('/your-endpoint', { method: 'GET' })  
    .then(() => window.location.href = url)  
    .catch(console.error);
}

function handlePhonemeClick(word, phoneme) {
    console.log('Clicked phoneme:', phoneme);
}

function main() {
  const search_button = document.getElementById("search_button");
  const search_input = document.getElementById("search_input");
  search_input.addEventListener("keydown", (event) => {
    if(event.key === "Enter")
      handleInput();
  });
  search_button.addEventListener("click", () => handleInput());
}

document.addEventListener("DOMContentLoaded", () => {
    main();
});
