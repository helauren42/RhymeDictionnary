export class Word {
  constructor(_word, _phone, _vw, _conso) {
    this.word = _word;
    this.phonemes = _phone;
    this.vowels = _vw;
    this.consonants = _conso;
    this.blocks = [];
    this.makeBlocks();
    console.log(this.blocks);
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
}

// when clicked on phoneme button identify to wich block the phoneme belongs

export function parseWord(wordDict) {
  let word = wordDict["word"];
  let phonemes = wordDict["phonemes"];
  let vowels = wordDict["vowels"];
  let consonants = wordDict["consonants"];
  return new Word(word, phonemes, vowels, consonants);
} 
