# -*- coding: utf-8 -*-

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@microsoft.com
#
# This demo is based on the Azure Cognitive Services Text Analytics Quick Starts
# 
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python-sdk

##################### FIRST: MOVE ALL TO MLHUB UTILS!!!!

##################### THEN: MOVE ALL TO USING PYTHON SDK!!!!!!

from mlhub.pkg import azkey, mlask, mlcat

mlcat("Azure Text Analytics", """\
Welcome to a demo of the pre-built models for Text Analytics provided
through Azure's Cognitive Services. This service extracts information
from text that we supply to it, providing information such as the
language, key phrases, sentiment (0-1 as negative to positive), and
entities.
""")

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

import sys
import os
import pickle
import requests

from textwrap import fill
from pprint import pprint

# pip3 install --upgrade --user azure-cognitiveservices-language-textanalytics

#from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
#from msrest.authentication import CognitiveServicesCredentials

# Constants.

CANNED_PKL = "canned.pkl"
live = True

# ----------------------------------------------------------------------
# Request subscription key and endpoint from user.
# ----------------------------------------------------------------------

SERVICE = "Text Analytics"
KEY_FILE  = os.path.join(os.getcwd(), "private.txt")

key, endpoint = azkey(KEY_FILE, SERVICE, verbose=False)#, basename=True)
######################## ADD BASENAME RETURNS THE BASE URL NOT FULL PATH

# Ensure endpoint ends in /

if endpoint[len(endpoint)-1] != "/": endpoint = endpoint + "/"

# Handle canned demonstration.
    
if len(key) == 0:
    live = False
    with open(CANNED_PKL, 'rb') as f:
        languages, sentiments, key_phrases, entities = pickle.load(f)
    sys.stdout.write("""
No subscription key was provided so we will continue with a canned
demonstration. The analyses from the cloud through the API have previously
been captured and so we will use them.
""")
    
mlask(end="\n")

mlcat("Language Information", """\
We will first demonstrate the automated identification of language. Below
are a few "documents" in different languages which are passed on to the 
cloud for processing using the following language API URL:
""")

language_api_url = endpoint + "languages"
print(language_api_url + "\n")

# 6 to 10 come from http://www.columbia.edu/~fdc/utf8/index.html

mlask()

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

if live:
    headers   = {"Ocp-Apim-Subscription-Key": key}
    response  = requests.post(language_api_url, headers=headers, json=documents)
    languages = response.json()

print("")

for d, l in zip(documents['documents'], languages['documents']):
    id = d['id']
    print("{} {}".format(id, d['text']))
    dl = l['detectedLanguages'][0]
    print("  This is {} ({}) with score of {}.".
          format(dl['name'], dl['iso6391Name'], dl['score']))
    if id == "5":
        print("  NOTE: the text is rather jumbled hence a lower score.")
    elif id == "8":
        print("  NOTE: a little tricky as it is actually Javanese.")
    elif id == "10":
        print("  NOTE: yes it is actually Ye Olde English.")
    print("")

mlask(end="\n")

mlcat("Sentiment Analysis", """\
Now we look at an analysis of the sentiment of the document/text. This is
done so by passing the text of the text on to the sentiment API URL
shown below for processing in the cloud. The results are returned as a number
between 0 and 1 with 0 being the most negative and 1 being the most positive.
""")

sentiment_api_url = endpoint + "sentiment"
print(sentiment_api_url)

mlask(begin="\n")

documents = {'documents' : [
  {'id': '1', 'language': 'en', 'text': 'I had a wonderful experience! The rooms were wonderful and the staff were helpful.'},
  {'id': '2', 'language': 'en', 'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},  
  {'id': '3', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},  
  {'id': '4', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
]}

if live:
    headers   = {"Ocp-Apim-Subscription-Key": key}
    response  = requests.post(sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()

print("")

for d, s in zip(documents['documents'], sentiments['documents']):
    id = d['id']
    print("{} {}".format(id, fill(d['text'], subsequent_indent="  ")))
    print("  This has a sentiment rating of {0:.2f}.\n".format(s['score']))

mlask(end="\n")

mlcat("Key Phrases", """\
We are often interested, for further analysis, in the key phrases found in
the text. Here we extract what are considered to be the key phrases from 
the text. Again, the text is passed on to the cloud through the API
at the URL below.
""")

key_phrase_api_url = endpoint + "keyPhrases"
print(key_phrase_api_url)

mlask(begin="\n")

documents = {'documents' : [
  {'id': '1', 'language': 'en', 'text': 'I had a wonderful experience! The rooms were wonderful and staff helpful.'},
  {'id': '2', 'language': 'en', 'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},  
  {'id': '3', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},  
  {'id': '4', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
]}

if live:
    headers   = {'Ocp-Apim-Subscription-Key': key}
    response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
    key_phrases = response.json()

print("")

for d, kp in zip(documents['documents'], key_phrases['documents']):
    id = d['id']
    print("{} {}".format(id, fill(d['text'], subsequent_indent="  ")))
    print("  The key phrases here are: {}.\n".format(kp['keyPhrases']))

mlask(end="\n")

mlcat("Entities", """\
Our final demonstration identifies the entities refered to in the text.
As a bonus the API generates a link to Wikipedia for more information! As 
above, the text is passed on to the cloud through the API at the URL below.
""")

entity_linking_api_url = endpoint + "entities"
print(entity_linking_api_url)

mlask(begin="\n", end="\n")

documents = {'documents' : [
    {'id': '1', 'text':
     'Jeff bought three dozen eggs because there was a 50% discount.'},
    {'id': '2', 'text':
     'The Great Depression began in 1929. By 1933, the GDP in America fell by 25%.'},
    {'id': '3', 'text':
     'I had a wonderful trip to Singapore and enjoyed seeing the Gardens by the Bay!'}
]}

if live:
    headers  = {"Ocp-Apim-Subscription-Key": key}
    response = requests.post(entity_linking_api_url, headers=headers, json=documents)
    entities = response.json()

for d, es in zip(documents['documents'], entities['documents']):
    id = d['id']
    print('{} {}'.format(id, fill(d['text'], subsequent_indent="  ")))
    for e in es['entities']:
        print("  {}: {}.".format(e['name'], e['type']))
    print("")

mlask(end="\n")

# This is how we save the responses for the canned demonstration.
# If the documents above change we need a new can of pickles.

if False:
    import pickle
    with open(CANNED_PKL, 'wb') as f:
        pickle.dump([languages, sentiments, key_phrases, entities], f)
