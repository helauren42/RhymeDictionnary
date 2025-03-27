export class Word {
  constructor(_word, _phone, _vw, _conso) {
    this.word = _word;
    this.phonemes = _phone;
    this.vowels = _vw;
    this.consonants = _conso;
    this.blocks = [];
    this.makeBlocks();
  }
  isVowel(phoneme) {
    if (this.vowels.includes(phoneme))
      return true;
    return false;
  }
  makeBlocks() {
    let i = 0;
    let previous_vowel = true;
    while (i < this.phonemes.length) {
      if (previous_vowel && this.isVowel(this.phonemes[i])) {
        this.blocks.push([""]);
      }
      if (this.isVowel(this.phonemes[i])) {
        this.blocks.push([this.phonemes[i]]);
        previous_vowel = true;
      }
      else {
        // is consonant
        if (previous_vowel) {
          this.blocks.push([this.phonemes[i]]);
        }
        else {
          this.blocks[this.blocks.length - 1].push(this.phonemes[i]);
        }
        previous_vowel = false;
      }
      i++;
    }
  }
  getPhonemeDuplicateIndex(phoneme, phoneme_index) {
    if (phoneme_index == 0)
      return 0;
    let ret = 0;
    for (let i = phoneme_index - 1; i >= 0; i--) {
      if (this.phonemes[i] == phoneme)
        ret++;
    }
    return ret;
  }
  getBlockIndex(phoneme, phoneme_index) {
    let phoneme_duplicate_index = this.getPhonemeDuplicateIndex(phoneme, phoneme_index);
    let count = 0;
    // console.log("dupe index: ", phoneme_duplicate_index);
    for (let i = 0; i < this.blocks.length; i++) {
      if (this.blocks[i].includes(phoneme)) {
        if (count == phoneme_duplicate_index)
          return i;
        count++;
      }
    }
    throw Error("get block index did not find block index");
  }
  hasBlock(block_index, phoneme) {
    if (block_index >= this.blocks.length)
      return false;
    return this.blocks[block_index].includes(phoneme);
  }
}

// when clicked on phoneme button identify to wich block the phoneme belongs

export function parseWord(wordDict) {
  let word = wordDict["word"];
  let phonemes = wordDict["phonemes"];
  let vowels = wordDict["vowels"];
  let consonants = wordDict["consonants"];
  return new Word(word, phonemes, vowels, consonants);
} 
