import wikipedia

def findpage(page_tag = 'Путин', lang = 'ru'):
    if (lang == 'en'): pass
    else: 
        try:
            wikipedia.set_lang(lang)
        except: 
            return 'Неверный язык'

    search_terms = ', '.join(wikipedia.search(page_tag, results=11))
    search_terms = search_terms[search_terms.find(' ')+1:]

    try:
        getpage = wikipedia.page(page_tag, auto_suggest=False)
        sumtext = getpage.content
        return(sumtext[:sumtext.find('\n')]+'\n\n'+'Ссылка на статью: '+getpage.url)
    except (wikipedia.exceptions.DisambiguationError) as wikidiserror:
        return('У этого тега несколько значений. Возможно вы имели в виду: '+search_terms)
    except (wikipedia.exceptions.PageError) as wiki_pageerror:
        return('Страница не найдена')