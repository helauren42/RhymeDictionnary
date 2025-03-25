const HOST = "http://127.0.0.1:"
let current_word = "";
let clicked_phoneme_indexes = [];
let g_list_of_rhymes = []

class Word {
  constructor() {
    let word = "";
    let phonemes = [];
    let vowels = [];
    let consonants = [];
    let particles = [];
  }
  makeParticles() {}
}

class PhonemeSearch {
  constructor() {
    let rhymes_list = [];
  }
  handlePhonemeClick(word, phoneme, phonemes, phoneme_index) {
    // phoneme_index 0 is the last phoneme of the word
    let button = document.getElementById("phoneme-btn" + phoneme_index);
  
    let current_word = word;
    console.log("current word: ", current_word);
    console.log("Clicked phoneme:", phoneme);
    console.log("Phoneme index:", phoneme_index);
    console.log("Phonemes:", phonemes);
    console.log("PRE click indexes: ", clicked_phoneme_indexes);
  
    if (button.className == "phoneme-btn") {
      console.log("adding");
      button.classList.remove("phoneme-btn");
      button.classList.add("active-btn");
      clicked_phoneme_indexes.push(parseInt(phoneme_index));
    } else {
      console.log("removing");
      button.classList.remove("active-btn");
      button.classList.add("phoneme-btn");
      clicked_phoneme_indexes = clicked_phoneme_indexes.filter(
        (index) => index != parseInt(phoneme_index),
      );
    }
    console.log("POST clicked indexes: ", clicked_phoneme_indexes);
  }
}

let phoneme_search = new PhonemeSearch();

function handleInput() {
  const search_input = document.getElementById("search_input");
  if (search_input.value.length == 0) {
    console.log("input is empty string");
    return;
  }
  let url = HOST + window.location.port + "/search/";
  url += search_input.value;
  fetch("/", { method: "GET" })
    .then(() => (window.location.href = url))
    .catch(console.error);
}

function main() {
  const search_button = document.getElementById("search_button");
  const search_input = document.getElementById("search_input");
  const has_rhymes_list = document.getElementById("rhymes_list");
  if(has_rhymes_list){
    const searched_word_baby = document.getElementById("searched_word_baby");
    let url = HOST + window.location.port + "/getrhymeslist/" + searched_word_baby.outerText;
    data = ""
    fetch(url)
    .then(response => response.json())
    .then(data => {
      resp = data;
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
  search_input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") handleInput();
  });
  search_button.addEventListener("click", () => handleInput());
}

document.addEventListener("DOMContentLoaded", () => {
  main();
});
