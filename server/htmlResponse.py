from dictionnary import Word

class HtmlResponse():
    async def buildSearchResultsPage(self, wordObj: Word, rhymes: list[Word]) -> str:
        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>RhymeDictionnary</title>
            <link rel="stylesheet" href="/static/css/index.css">
        </head>'''

        '''
        <body>
            <h1>Rhymes for "{wordObj.word}"</h1>
            <div class="searched-word-phonemes">
        '''

        phoneme_index = 0
        for phoneme in wordObj.phonemes:
            html_content += f'''
                <button class="phoneme-btn{phoneme_index}" onclick="handlePhonemeClick({wordObj.word}, '{phoneme}')">{phoneme}</button>
            '''
            phoneme_index += 1

        html_content += '''
            </div>
            <ul>
        '''

        for rhyme in rhymes:
            html_content += f'''
                <li>{rhyme.word}<span class="phonemes">({" ".join(rhyme.phonemes)})</span></li>
            '''
        html_content += '''
            </ul>
        </body>
        </html>
        '''

        return html_content
