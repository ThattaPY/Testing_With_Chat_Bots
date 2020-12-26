from selenium import webdriver
from collections import Counter
import spacy

driver = webdriver.Chrome(executable_path='drivers/chromedriver.exe')
nlp = spacy.load("/Users/toore/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0/LocalCache/local-packages/Python38/site-packages/es_core_news_sm/es_core_news_sm-2.3.1")

driver.get('https://es.wikipedia.org/wiki/hipnosis')
searched = []
urls = [driver.current_url]

for swing in range(0, 5):

    h2 = driver.find_element_by_id('content')
    text = h2.text
    doc = nlp(text)

    nouns = [token.text for token in doc if
             token.is_stop is not True and token.is_punct is not True and token.pos_ == "NOUN"]
    noun_freq = Counter(nouns)
    common_nouns = noun_freq.most_common(20)
    c = 0
    next_search = common_nouns[c][0]
    print("Inicial: " + next_search)

    ok = False
    while not ok:
        if next_search in searched:
            c += 1
            next_search = common_nouns[c][0]
            print("BUCLE: " + next_search)
            if c == len(common_nouns):
                next_search = 'a'
                searched.append(next_search)
                ok = True
        else:
            searched.append(next_search)
            ok = True
    c = 0
    ok2 = False

    while not ok2:
        links = driver.find_elements_by_partial_link_text(next_search)


        if True:
            while c + 1 < len(links):
                url = links[c].get_property('href')
                if url not in urls:
                    if ".pdf" not in url and driver.current_url not in url:
                        urls.append(driver.current_url)
                        print(url)
                        if url:
                            driver.get(url)
                            ok2 = True
                        else:
                            ok2 = True
                    else:
                        c += 1

                else:
                    c += 1

                if c + 1 == len(links):
                   ok2 = True











'''
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
    print('-')

for ent in doc.ents:
    print(ent.text, ent.label_)
    print('-')

c = 1
for token in doc:
    print(token.text, 'has vector: ', token.vector_norm,)
    print(c)
    c += 1

print([t.text for t in doc])

c = 1
noun_chunks = list(doc.noun_chunks)
for element in noun_chunks:
    print(noun_chunks[c].text)
    c += 1

vectors = list(doc)

for word in vectors:
    print(word.vector)
    print('-')
'''
