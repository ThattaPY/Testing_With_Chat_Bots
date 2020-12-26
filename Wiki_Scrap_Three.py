from selenium import webdriver
from collections import Counter
import spacy
import random


def search_common(doc, driver, prohibited_in_url):
    nouns = [token.text for token in doc if
             token.is_stop is not True and token.is_punct is not True and token.pos_ == "NOUN"]
    noun_freq = Counter(nouns)
    common_nouns = noun_freq.most_common(25)
    c = 0
    next_search = common_nouns[c][0]
    links = driver.find_elements_by_partial_link_text(next_search)
    print(next_search)

    while True:
        c += 1
        next_search = common_nouns[c][0]
        links = driver.find_elements_by_partial_link_text(next_search)
        if links:
            url = links[0].get_property('href')
            b = 0
            while url in driver.current_url or 'https://es.wikipedia.org/wiki/' not in url or any(
                string in url for string in prohibited_in_url):
                b += 1
                url = links[b].get_property('href')
                break

    return url


driver = webdriver.Chrome(executable_path='drivers/chromedriver2.exe')
nlp = spacy.load(
    "/Users/toore/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0/LocalCache/local-packages"
    "/Python38/site-packages/es_core_news_sm/es_core_news_sm-2.3.1")

prohibited_in_url = [".pdf", ".jpg", '.png', '.gif', '.svg', '=edit', "wiki/Ayuda:", "wiki/Plantilla:", '(desambiguaci%C3%B3n)', 'Wikipedia:', 'Portal:', 'Especial:CategoryTree']

site = 'https://es.wikipedia.org/wiki/programacion'
words_historial = []
driver.get(site)
historial = [driver.current_url]
content = driver.find_element_by_id('bodyContent')
text = content.text
doc = nlp(text)
url = search_common(doc, driver, prohibited_in_url)
driver.get(url)
