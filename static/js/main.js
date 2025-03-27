import { PhonemeSearch } from './PhonemeSearch.js';

const HOST = "http://127.0.0.1:"
let phoneme_search = new PhonemeSearch();

const MakeRequest = {
  handleInput() {
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
  },
  async fetchRhymes() {
    const searched_word_baby = document.getElementById("searched_word_baby");
    let url = HOST + window.location.port + "/getrhymeslist/" + searched_word_baby.outerText;

    let response = await fetch(url);
    const data = await response.json();
    return data;
  },
  async fetchWord() {
    const searched_word_baby = document.getElementById("searched_word_baby");
    let url = HOST + window.location.port + "/getword/" + searched_word_baby.outerText;

    let response = await fetch(url);
    const data = await response.json();
    return data;
  }
}

function removeLi() {
  const rhymes_list = document.getElementById("rhymes_list");
  rhymes_list.innerHTML = "";
}

function addLi() {
  const rhymes_list = document.getElementById("rhymes_list");
  for (let obj of phoneme_search.filtered_rhyme_list) {
    rhymes_list.innerHTML += "<li>" + obj[0] + '<span class="phonemes">(' + obj[1] + ")";
    rhymes_list.innerHTML += "</span></li>"
  }
}

function applyPhenomes() {
  phoneme_search.search();
  if (phoneme_search.filtered_rhyme_list.length == phoneme_search.rhymes_list.length) {
    return;
  }
  removeLi();
  addLi();
}

async function main() {
  const search_button = document.getElementById("search_button");
  const apply_button = document.getElementById("apply_button");
  const search_input = document.getElementById("search_input");
  const has_rhymes_list = document.getElementById("rhymes_list");
  const phoneme_buttons = document.getElementsByClassName("phoneme-btn");
  search_input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") MakeRequest.handleInput();
  });
  search_button.addEventListener("click", () => MakeRequest.handleInput());
  if (has_rhymes_list) {
    let rhymes = await MakeRequest.fetchRhymes();
    phoneme_search.parseRhymesList(rhymes);
    let word = await MakeRequest.fetchWord();
    phoneme_search.parseSearchedWord(word);
    apply_button.addEventListener("click", () => applyPhenomes());
    for (let i = 0; i < phoneme_buttons.length; i++) {
      phoneme_buttons[i].addEventListener("click", function() {
        phoneme_search.handlePhonemeClick(
          this.textContent,
          this.id
        )
      })
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  main();
});

