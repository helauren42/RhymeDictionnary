import { Word, parseWord } from "./Word.js";

export class PhonemeSearch {
  constructor() {
    this.rhymes_list = [];
    this.searched_word = null;
    this.clicked_phoneme_indexes = [];
    this.filtered_rhyme_list = [];
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
  }
  parseSearchedWord(_searched_word_dict) {
    this.searched_word = parseWord(_searched_word_dict);
  }
  handlePhonemeClick(phoneme, phoneme_index) {
    // phoneme_index 0 is the last phoneme of the word
    let button = document.getElementById(phoneme_index);

    console.log("Clicked phoneme:", phoneme);
    console.log("Phoneme index:", phoneme_index);

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
  }
  phenomes_str(listPhonemes) {
    let str = "";
    for (let string of listPhonemes)
      str = string + " " + str;
    str = str.trimEnd();
    return str;
  }
  search() {
    this.filtered_rhyme_list = [];
    let searchFor = {};
    for (let index of this.clicked_phoneme_indexes) {
      let phoneme = this.searched_word.phonemes[index];
      let block_index = this.searched_word.getBlockIndex(phoneme, index);
      searchFor[block_index] = phoneme;
    }
    console.log(searchFor);
    for (let word of this.rhymes_list) {
      let add = true;
      for (let [block_index, phoneme] of Object.entries(searchFor)) {
        // console.log("word object normally: ", word);
        if (!word.hasBlock(block_index, phoneme)) {
          add = false;
          break;
        }
      }
      if (add)
        this.filtered_rhyme_list.push([word.word, this.phenomes_str(word.phonemes)]);
    }
  }
}
