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
            <link rel="stylesheet" href="/static/css/index.css">
        </head>'''

    @staticmethod
    async def getPhonemeButtons(wordObj: Word):
        phoneme_index = 0
        phoneme_buttons = ""
        for phoneme in wordObj.phonemes:
            phoneme_buttons = f''' <button class="phoneme-btn{phoneme_index}" onclick="handlePhonemeClick({wordObj.word}, '{phoneme}')">{phoneme}</button> ''' + phoneme_buttons
            phoneme_index += 1
        return phoneme_buttons

    @staticmethod
    async def getRhymeList(rhymes: list[Word]) -> str:
        content = f'''<ul>'''
        logging.info(f"RHYMES:\n{rhymes}")
        for rhyme in rhymes:
            content += f'''<li>{rhyme.word}<span class="phonemes">({" ".join(rhyme.phonemes)})</span></li>'''
        content += f'''</ul>'''
        logging.info(f"--- rhyme list: {content}")
        return content

    @staticmethod
    async def buildSearchResultsPage(wordObj: Word, rhymes: list[Word]) -> str:
        html_content = await HtmlResponse.getHead()
        html_content += f'''
        <body>
            <h1>Rhymes for "{wordObj.word}"</h1>
            <div class="searched-word-phonemes">
        '''
        phoneme_buttons = await HtmlResponse.getPhonemeButtons(wordObj)
        html_content += phoneme_buttons + ''' </div>'''

        html_content += await HtmlResponse.getRhymeList(rhymes)

        html_content += f'''</body></html>'''
        logging.info(html_content)
        return html_content
