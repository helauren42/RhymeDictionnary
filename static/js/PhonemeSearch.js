import { Word, parseWord } from "./Word.js";

export class PhonemeSearch {
  constructor() {
    this.rhymes_list = [];
    this.searched_word = null;
    this.clicked_phoneme_indexes = [];
  }

  /**
   * @param {Array<{word: string, phonemes: string[], vowels: string[], consonants: string[]}>} data
   */
  parseRhymesList(data) {
    for (let i = 0; i < data.length; i++) {
      try {
        let wordObj = parseWord(data[i]);
        this.rhymes_list.push(wordObj);
      } catch (error) {
        console.error("Error parsing word:", data[i], error);
      }
    }
    // console.log("PARSED RHYMES LIST: ", this.rhymes_list);
  }
  parseSearchedWord(_searched_word_dict) {
    this.searched_word = parseWord(_searched_word_dict);
  }
  handlePhonemeClick(word, phoneme, phonemes, phoneme_index) {
    // phoneme_index 0 is the last phoneme of the word
    let button = document.getElementById(phoneme_index);
    let current_word = word;

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
