from nltk.corpus import stopwords
import spacy
from collections import Counter
from selenium import webdriver

spanish_stopwords = set(stopwords.words('spanish'))
nlp = spacy.load("/Users/toore/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0/LocalCache/local-packages/Python38/site-packages/es_core_news_sm/es_core_news_sm-2.3.1")
driver = webdriver.Chrome(executable_path='drivers/chromedriver.exe')


def tokenize_phrase(phrase):
    parsed_phrase = nlp(phrase)
    for token in parsed_phrase:
        if token.is_punct or token.is_stop or token.text.lower() in spanish_stopwords:
            continue
        yield token.lemma_.lower()


driver.get('https://es.wikipedia.org/wiki/Deportes_electr%C3%B3nicos')

h2 = driver.find_element_by_class_name('mw-parser-output')
texto = h2.text

# contador
word_counter = Counter()

for xpresion in texto:
    word_counter.update(tokenize_phrase(xpresion))
