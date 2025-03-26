export class Word {
  constructor(_word, _phone, _vw, _conso) {
    this.word = _word;
    this.phonemes = _phone;
    this.vowels = _vw;
    this.consonants = _conso;
    this.blocks = this.makeBlocks();
    this.particles = this.makeParticles();
  }
  isVowel(phoneme) {
    if (this.vowels.includes(phoneme))
      return true;
    return false;
  }
  makeBlocks() {
    let pos = 0;
    let previousIsVowel = true;
    let ret = []
    for (let phoneme of this.phonemes) {
      if (this.isVowel(phoneme) && (pos == 0 || previousIsVowel)) {
        ret.push("");
        ret.push(phoneme);
      }
    }
    return ret;
  }
  makeParticles() {
    let pos = 0;
    let ret = [];
    for (let block of this.blocks) {
      if (this.isVowel(block)) {
        ret.push(block);
      }
    }
    return ret;
  }
}

