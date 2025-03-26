export class Word {
  constructor(_word, _phone, _vw, _conso) {
    this.word = _word;
    this.phonemes = _phone;
    this.vowels = _vw;
    this.consonants = _conso;
    this.blocks = this.makeBlocks();
  }
  isVowel(phoneme) {
    if (this.vowels.includes(phoneme))
      return true;
    return false;
  }
}

