from difflib import HtmlDiff
from dictionnary import Word
import logging

class HtmlResponse():
    @staticmethod
    async def getHead():
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>RhymeDictionnary</title>
            <link rel="stylesheet" href="../static/css/index.css">
            <script type="module" src="../static/js/main.js"></script>
        </head>'''
    
    @staticmethod
    async def getPhonemeButtons(wordObj: Word):
        phoneme_index = 0
        phoneme_buttons = ""
        for phoneme in wordObj.phonemes:
            phoneme_buttons = f''' <button class="phoneme-btn" id="{phoneme_index}" >{phoneme}</button> ''' + phoneme_buttons
            phoneme_index += 1
        return phoneme_buttons

    @staticmethod
    async def getRhymeList(rhymes: list[Word]) -> str:
        content = f'''<ul id="rhymes_list">'''
        logging.info(f"RHYMES:\n{rhymes}")
        for rhyme in rhymes:
            phonemes_str = ""
            for phoneme in rhyme.phonemes:
                phonemes_str = phoneme + " " + phonemes_str
            content += f'''<li>{rhyme.word}<span class="phonemes">({phonemes_str.strip()})</span></li>'''
        content += f'''</ul>'''
        logging.info(f"--- rhyme list: {content}")
        return content

    @staticmethod
    async def buildSearchResultsPage(wordObj: Word, rhymes: list[Word]) -> str:
        html_content = await HtmlResponse.getHead()
        html_content += f'''<body><h1 id="searched_word_baby">{wordObj.word}</h1><div id="searched-word-phonemes">'''
        phoneme_buttons = await HtmlResponse.getPhonemeButtons(wordObj)
        html_content += phoneme_buttons + '''<button id="apply_button">apply</button></div>'''

        html_content += f'''<div id="search_block"><input type="search" placeholder="Find rhymes" id="search_input">
        <button id="search_button">search</button></div>'''

        html_content += await HtmlResponse.getRhymeList(rhymes)

        html_content += f'''</body></html>'''
        logging.info(html_content)
        return html_content
