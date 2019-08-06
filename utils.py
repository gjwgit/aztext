# Helper Function to do the work.

import requests

def analyseLanguage(txt, key, endpoint):
    documents = { 'documents': [{ 'id': '1', 'text': txt }]}
    url       = endpoint + "languages"
    headers   = {"Ocp-Apim-Subscription-Key": key}
    response  = requests.post(url, headers=headers, json=documents)
    languages = response.json()

    l    = languages['documents'][0]
    dl   = l['detectedLanguages'][0]
    lang = dl['iso6391Name']

    print(f"{dl['score']},{lang},", end="")

def analyseSentiment(txt, key, endpoint):
    # Indonesian is not a supported language.
    documents  = { 'documents': [{ 'id': '1', 'language': lang, 'text': txt }]}
    url        = endpoint + "sentiment"
    headers    = {"Ocp-Apim-Subscription-Key": key}
    response   = requests.post(url, headers=headers, json=documents)
    sentiments = response.json()

    sep = ""
    for s in sentiments['documents']:
        print(f"{sep}{s['score']:0.2f}", end="")
        sep=":"
    print(",", end="")

