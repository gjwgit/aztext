# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# This demo is based on the Azure Cognitive Services Text Analytics Quick Starts
# 
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python
#
# TODO
# * If no key then just dummy the results!

print("""====================
Azure Text Analytics
====================

Welcome to a demo of the pre-built models for Text Analytics provided
through Azure's Cognitive Services. This service extracts information
from text that we supply to it, providing information such as the
language, key phrases, sentiment (0-1 as negative to positive
sentiment), and entities (person, organisation, a quantity, date and
time, a URL, or an email address).
""")

# Import the required libraries.

import sys
import os
import requests
from pprint import pprint

# Prompt the user for the key and region and save into private.py for
# future runs of the model. The contents of that file is:
#
# subscription_key = "a14d...ef24"
# assert subscription_key
# region = "southeastasia"

fname = "private.py"

if os.path.isfile(fname):
    print("""The following file has been found and is assumed to contain
an Azure Text Analytics subscription key and region. We will load 
the file and use this information.

""" + os.getcwd() + "/" + fname)
    exec(open(fname).read())
else:
    print("""An Azure resource is required to access this service (and to run this
demo). See the README for details of a free subscription. Then you can
provide the key and the region information here.

If you don't have a key and want to review the canned examples rather
than work with the live examples, you can indeed continue.
""")
    sys.stdout.write("Please enter your Text Analytics subscription key: ")
    subscription_key = input()
    assert subscription_key

    sys.stdout.write("Please enter your region (e.g., southeastasia): ")
    region = input()

    ofname = open(fname, "w")
    ofname.write("""subscription_key = "{}"
assert subscription_key
region = "{}"
    """.format(subscription_key, region))
    ofname.close()

    print("""
I've saved that information into the file:

""" + os.getcwd() + "/" + fname)
    
sys.stdout.write("""
Press Enter to continue: """)
answer = input()

cognitive_services_url = "https://" + region + ".api.cognitive.microsoft.com"
text_analytics_base_url = cognitive_services_url + "/text/analytics/v2.0/"

print("""
====================
Language Information
====================

We will first demonstrate the automated identification of language. Below
are a few "documents" in different languages which are passed on to the 
language API URL for processing in the cloud:
""")

language_api_url = text_analytics_base_url + "languages"
print(language_api_url + "\n")

# 6 to 10 come from http://www.columbia.edu/~fdc/utf8/index.html

sys.stdout.write("""Press Enter to continue: """)
answer = input()

documents = { 'documents': [
    { 'id': '1', 'text': 'This line is some text as a sample document written in English.' },
    { 'id': '2', 'text': 'Este es un document escrito en Español.' },
    { 'id': '3', 'text': '这是一个用中文写的文件' },
    { 'id': '4', 'text': 'Nor for itself hath any care.' },
    { 'id': '5', 'text': 'Nor for itself es un escrito 这是.' },
    { 'id': '6', 'text': 'Τη γλώσσα μου έδωσαν ελληνική' },
    { 'id': '7', 'text': 'मैं काँच खा सकता हूँ और मुझे उससे कोई चोट नहीं पहुंचती.' },
    { 'id': '8', 'text': 'Aku isa mangan beling tanpa lara.' }, # Actually Javanese rather than Indonesian.
    { 'id': '9', 'text': 'ฉันกินกระจกได้ แต่มันไม่ทำให้ฉันเจ็บ' },
    { 'id': '10', 'text': 'Ich canne glas eten and hit hirtiþ me nouȝt.' },
]}

headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
response  = requests.post(language_api_url, headers=headers, json=documents)
languages = response.json()

print("")

for d, l in zip(documents['documents'], languages['documents']):
    id = d['id']
    print(d['text'])
    dl = l['detectedLanguages'][0]
    print("  This is {} ({}) with score of {}.\n".
          format(dl['name'], dl['iso6391Name'], dl['score']))
    if id == "5":
        sys.stdout.write("""==> That one was purposely jumbled. Note the score.

Press Enter to continue: """)
        answer = input()
        print("")
    elif id == "8":
        sys.stdout.write("""==> That one is a little tricky. It is actually Javanese though it is
==> probably identified as Indonesian by most text analytics.

Press Enter to continue: """)
        answer = input()
        print("")

sys.stdout.write("""==> That's the end of the language examples.

Press Enter to continue: """)
answer = input()

print("""
==================
Sentiment Analysis
==================

Now we look at an analysis of the sentiment of the document/text. This is
done so by passing the text of the document on to the sentiment API URL
shown below for processing in the cloud. The results are returned as a number
between 0 and 1 with 0 being the most negative and 1 being the most positive.
""")

sentiment_api_url = text_analytics_base_url + "sentiment"
print(sentiment_api_url)

sys.stdout.write("""
Press Enter to continue: """)
answer = input()

documents = {'documents' : [
  {'id': '1', 'language': 'en', 'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
  {'id': '2', 'language': 'en', 'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},  
  {'id': '3', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},  
  {'id': '4', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
]}

headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
response  = requests.post(sentiment_api_url, headers=headers, json=documents)
sentiments = response.json()

print("")

for d, s in zip(documents['documents'], sentiments['documents']):
    id = d['id']
    print(d['text']) #WRAP THE TEXT
    # ADD ENGLISH TRANSALTION ...
    print("\n  This has a sentiment rating of {0:.2f}.\n".format(s['score']))

sys.stdout.write("""That's the end of the sentiment examples. Press Enter to continue: """)
answer = input()

print("""
===========
Key Phrases
===========

We are often interested, for further analysis, in the key phrases of a 
document. Here we extract what are considered to be the key phrases of
the document. Again, the text is passed on to the cloud through the API
at the URL below.
""")

key_phrase_api_url = text_analytics_base_url + "keyPhrases"
print(key_phrase_api_url)

sys.stdout.write("""
Press Enter to continue: """)
answer = input()

documents = {'documents' : [
  {'id': '1', 'language': 'en', 'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
  {'id': '2', 'language': 'en', 'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},  
  {'id': '3', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},  
  {'id': '4', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
]}
headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
key_phrases = response.json()

print("")

for d, kp in zip(documents['documents'], key_phrases['documents']):
    id = d['id']
    print(d['text']) #WRAP THE TEXT
    # ADD ENGLISH TRANSALTION ...
    print("\n  The key phrases here are: {}.\n".format(kp['keyPhrases']))

sys.stdout.write("""That's the end of the key phrases. Press Enter to continue: """)
answer = input()

print("""
========
Entities
========

Our final demonstration identifies the entities refered to in the document.
As a bonus it also links to Wikipedia for more information! As above, the
text is passed on to the cloud through the API at the URL below.
""")

entity_linking_api_url = text_analytics_base_url + "entities"
print(entity_linking_api_url)

sys.stdout.write("""
Press Enter to continue: """)
answer = input()

print("")

documents = {'documents' : [
    {'id': '1', 'text':
     'Jeff bought three dozen eggs because there was a 50% discount.'},
    {'id': '2', 'text':
     'The Great Depression began in 1929. By 1933, the GDP in America fell by 25%.'},
    {'id': '3', 'text':
     'I had a wonderful trip to Singapore and enjoyed seeing the Gardens by the Bay!'}
]}

headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
response  = requests.post(entity_linking_api_url, headers=headers, json=documents)
entities = response.json()

for d, es in zip(documents['documents'], entities['documents']):
    id = d['id']
    print(d['text']) #WRAP THE TEXT
    for e in es['entities']:
        print("  {}:\t{}.".format(e['name'], e['wikipediaUrl']))
    print("")

sys.stdout.write("""Press Enter to finish: """)
answer = input()

