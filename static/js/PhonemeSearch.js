import { Word } from "./Word.js";

export class PhonemeSearch {
  constructor() {
    this.rhymes_list = [];
    this.searched_word = null;
    this.clicked_phoneme_indexes = [];
  }
  parseRhymesList(data) {
  }
  parseSearchedWord(_searched_word) {
    console.log(_searched_word);
    let word = _searched_word["word"];
    let phonemes = _searched_word["phonemes"];
    let vowels = _searched_word["vowels"];

    let consonants = _searched_word["consonants"];
    console.log(phonemes);
    console.log(vowels);
    console.log(consonants);
    this.searched_word = new Word(word, phonemes, vowels, consonants);
  }
  handlePhonemeClick(word, phoneme, phonemes, phoneme_index) {
    // phoneme_index 0 is the last phoneme of the word
    let button = document.getElementById(phoneme_index);

    let current_word = word;
    console.log("current word: ", current_word);
    console.log("Clicked phoneme:", phoneme);
    console.log("Phoneme index:", phoneme_index);
    console.log("Phonemes:", phonemes);
    console.log("PRE click indexes: ", this.clicked_phoneme_indexes);

    if (button.className == "phoneme-btn") {
      button.classList.remove("phoneme-btn");
      button.classList.add("active-btn");
      this.clicked_phoneme_indexes.push(parseInt(phoneme_index));
    } else {
      button.classList.remove("active-btn");
      button.classList.add("phoneme-btn");
      this.clicked_phoneme_indexes = this.clicked_phoneme_indexes.filter(
        (index) => index != parseInt(phoneme_index),
      );
    }
    console.log("POST clicked indexes: ", this.clicked_phoneme_indexes);
  }
}
