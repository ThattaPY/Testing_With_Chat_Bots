from selenium import webdriver
from collections import Counter
import spacy
import random


def nlp_object():
    content = driver.find_element_by_id('bodyContent')
    text = content.text
    doc = nlp(text)
    return doc


def search_next_word(doc, historial, block, prohibited_in_url):
    doc = doc
    historial = historial
    nouns = [token.text for token in doc if
             token.is_stop is not True and token.is_punct is not True and token.pos_ == "NOUN"]
    noun_freq = Counter(nouns)
    common_nouns = noun_freq.most_common(30)
    c = 0

    next_search = common_nouns[c][0]

    links = block.find_elements_by_partial_link_text(next_search)
    if links:
        url = links[0].get_property('href')
        a = 0
        while url in driver.current_url or 'https://es.wikipedia.org/wiki/' not in url or any(
                string in url for string in prohibited_in_url):
            if a + 1 < len(links):
                a += 1
                url = links[a].get_property('href')
                if url not in historial:
                    return url


def search_next_link(historial, block, prohibited_in_url):
    links = block.find_elements_by_xpath("//a[@href]")
    historial = historial
    link_freq = Counter(links)
    common_links = link_freq.most_common(30)
    a = 0
    url = common_links[a][0].get_property('href')

    while driver.current_url in url or 'https://es.wikipedia.org/wiki/' not in url or any(
            string in url for string in prohibited_in_url):
        if a + 1 < len(common_links):
            a += 1
            url = common_links[a][0].get_property('href')
    if url not in historial:
        return url


def search_random(doc, block, prohibited_in_url):
    doc = doc
    nouns = [token.text for token in doc if
             token.is_stop is not True and token.is_punct is not True and token.pos_ == "NOUN"]
    noun_freq = Counter(nouns)
    common_nouns = noun_freq.most_common(30)
    c = len(common_nouns)
    next_search = common_nouns[random.randrange(c - 1)][0]

    links = block.find_elements_by_partial_link_text(next_search)
    if links:
        url = links[0].get_property('href')
        while driver.current_url in url or 'https://es.wikipedia.org/wiki/' not in url or any(
                string in url for string in prohibited_in_url):
            next_search = common_nouns[random.randrange(c - 1)][0]
            links = driver.find_elements_by_partial_link_text(next_search)
            i = 0
            while not links or i >= 10:
                next_search = common_nouns[random.randrange(c - 1)][0][:3]
                links = driver.find_elements_by_partial_link_text(next_search)
                i += 1

        if links:
            url = links[0].get_property('href')
        else:
            url = 'https://es.wikipedia.org/wiki/Wikipedia:Art%C3%ADculos_destacados'

    else:
        url = 'https://es.wikipedia.org/wiki/Wikipedia:Art%C3%ADculos_destacados'

    return url


def segundo_header(doc):
    h2 = driver.find_element_by_id("firstHeading").text
    nouns = [token.text for token in doc if
             token.is_stop is not True and token.is_punct is not True and token.pos_ == "NOUN"]
    noun_freq = Counter(nouns)
    common_nouns = noun_freq.most_common(7)
    return h2, common_nouns


driver = webdriver.Chrome(executable_path='drivers/chromedriver2.exe')
nlp = spacy.load(
    "/Users/toore/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0/LocalCache/local-packages"
    "/Python38/site-packages/es_core_news_sm/es_core_news_sm-2.3.1")

site = 'https://es.wikipedia.org/wiki/programacion'

driver.get(site)
salir = False

historial = [site]
content = driver.find_element_by_id('bodyContent')
text = content.text
doc = nlp(text)
encabezados_secundarios = [segundo_header(doc)]

prohibited_in_url = [".pdf", ".jpg", '.png', '.gif', '.svg', '=edit', "wiki/Ayuda:", "wiki/Plantilla:", '(desambiguaci%C3%B3n)', 'Wikipedia:', 'Portal:', 'Especial:CategoryTree']
c = 0
while not salir:
    content = driver.find_element_by_id('bodyContent')
    text = content.text
    doc = nlp(text)
    web = search_next_word(doc, historial, content, prohibited_in_url)
    if web in historial or not web:
        web = search_next_link(historial, content, prohibited_in_url)
        if web not in historial and web:
            historial.append(web)
            if 'https://es.wikipedia.org' in web:
                driver.get(web)
                encabezados_secundarios.append(segundo_header(doc))
            else:
                web = search_random(doc, content, prohibited_in_url)
                historial.append(web)
                driver.get(web)
                encabezados_secundarios.append(segundo_header(doc))

        else:
            w = 0
            while not web or w <= 3:
                web = search_random(doc, content, prohibited_in_url)
                w += 1
            if not web:
                web = 'https://es.wikipedia.org/wiki/Wikipedia:Art%C3%ADculos_destacados'
            historial.append(web)
            driver.get(web)
            encabezados_secundarios.append(segundo_header(doc))

    else:

        if 'https://es.wikipedia.org' in web:
            historial.append(web)
            driver.get(web)
            encabezados_secundarios.append(segundo_header(doc))

        else:
            q = 0
            while not web or q <= 3:
                web = search_random(doc, content, prohibited_in_url)
                q += 1
                if not web:
                    web = 'https://es.wikipedia.org/wiki/Wikipedia:Art%C3%ADculos_destacados'
            historial.append(web)
            driver.get(web)
            encabezados_secundarios.append(segundo_header(doc))
    c += 1
    if any(string in web for string in prohibited_in_url):
        web = 'https://es.wikipedia.org/wiki/Wikipedia:Art%C3%ADculos_destacados'
        driver.get(web)
    if c == 4 or historial.count('https://es.wikipedia.org/wiki/Wikipedia:Art%C3%ADculos_destacados') >= 3:
        salir = True

for h2 in encabezados_secundarios:
    print(h2)
