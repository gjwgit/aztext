# -*- coding: utf-8 -*-

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@microsoft.com
#
# Based on the Azure Cognitive Services Text Analytics Quick Starts
# 
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/
#   quickstarts/python
#   quickstarts/python-sdk

from mlhub.pkg import mlask, mlcat
from mlhub.utils import get_private

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

from textwrap import fill

# pip3 install --upgrade --user azure-cognitiveservices-language-textanalytics

from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

# ----------------------------------------------------------------------
# Request subscription key and endpoint from user.
# ----------------------------------------------------------------------

PRIVATE_FILE = "private.json"

path = os.path.join(os.getcwd(), PRIVATE_FILE)

private_dic = get_private(path, "aztext")

key = private_dic["Text Analytics"]["key"]

endpoint = private_dic["Text Analytics"]["endpoint"]

mlask(end="\n")

mlcat("Language Information", """\
We will first demonstrate the automated identification of language. Below
are a few "documents" in different languages which are passed on to the 
cloud for processing using the following language API URL:
""")

# Authenticate credentials and create a Text Analytics client.

credentials = CognitiveServicesCredentials(key)
client = TextAnalyticsClient(endpoint=endpoint, credentials=credentials)

# Determine Language

# 6 to 10 come from http://www.columbia.edu/~fdc/utf8/index.html

mlask(end="\n")

documents = [
    { 'id': '1', 'text': 'Text as a sample document written in English.' },
    { 'id': '2', 'text': 'Este es un document escrito en Español.' },
    { 'id': '3', 'text': '这是一个用中文写的文件' },
    { 'id': '4', 'text': 'Nor for itself hath any care.' },
    { 'id': '5', 'text': 'Nor for itself es un escrito 这是.' },
    { 'id': '6', 'text': 'Τη γλώσσα μου έδωσαν ελληνική' },
    { 'id': '7', 'text': 'मैं काँच खा सकता हूँ और मुझे उससे कोई चोट नहीं पहुंचती.' },
    # Actually the next is Javanese rather than Indonesian.
    { 'id': '8', 'text': 'Aku isa mangan beling tanpa lara.' },
    { 'id': '9', 'text': 'ฉันกินกระจกได้ แต่มันไม่ทำให้ฉันเจ็บ' },
    { 'id': '10', 'text': 'Ich canne glas eten and hit hirtiþ me nouȝt.' },
]

response = client.detect_language(documents=documents)

for d, r in zip(documents, response.documents):
    id = d['id']
    print("{} {}".format(id, d['text']))
    dl = r.detected_languages[0]
    print("  This is {} ({}) with score of {}.".
          format(dl.name, dl.iso6391_name, dl.score))
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

mlask(end="\n")

documents = [
  {'id': '1', 'language': 'en', 'text':
   'I had a wonderful experience! Rooms were wonderful and staff helpful.'},
  {'id': '2', 'language': 'en', 'text':
   'I had a terrible time at the hotel. The staff was rude and food awful.'},  
  {'id': '3', 'language': 'es', 'text':
   'Los caminos que llevan hasta Monte Rainier son espectaculares hermosos.'},
  {'id': '4', 'language': 'es', 'text':
   'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
]

response = client.sentiment(documents=documents)

for d, r in zip(documents, response.documents):
    id = d['id']
    print("{} {}".format(id, fill(d['text'], subsequent_indent="  ")))
    print("  This has a sentiment rating of {0:.2f}.\n".format(r.score))

mlask(end="\n")

mlcat("Key Phrases", """\
We are often interested, for further analysis, in the key phrases found in
the text. Here we extract what are considered to be the key phrases from 
the text. Again, the text is passed on to the cloud through the API
at the URL below.
""")

mlask()

documents = [
  {'id': '1', 'language': 'en', 'text':
   'I had a wonderful experience! The rooms wonderful and staff helpful.'},
  {'id': '2', 'language': 'en', 'text':
   'I had a terrible time at the hotel. The staff rude and the food awful.'},  
  {'id': '3', 'language': 'es', 'text':
   'Los caminos que llevan hasta Monte Rainier son espectaculares hermosos.'},
  {'id': '4', 'language': 'es', 'text':
   'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
]

response = client.key_phrases(documents=documents)

for d, r in zip(documents, response.documents):
    id = d['id']
    print("{} {}".format(id, fill(d['text'], subsequent_indent="  ")))
    print("  The key phrases here are: {}.\n".format(r.key_phrases))

mlask(end="\n")

mlcat("Entities", """\
Our final demonstration identifies the entities refered to in the text.
As a bonus the API generates a link to Wikipedia for more information! As 
above, the text is passed on to the cloud through the API at the URL below.
""")

mlask(end="\n")

documents = [
    {'id': '1', 'text':
     'Jeff bought three dozen eggs because there was a 50% discount.'},
    {'id': '2', 'text':
     'The Great Depression began in 1929. By 1933, the GDP in America fell by 25%.'},
    {'id': '3', 'text':
     'I had a wonderful trip to Singapore and enjoyed seeing the Gardens by the Bay!'}
]

response = client.entities(documents=documents)

for d, r in zip(documents, response.documents):
    id = d['id']
    print('{} {}'.format(id, fill(d['text'], subsequent_indent="  ")))
    for e in r.entities:
        print(f"  {e.name}: {e.type}.")
    print("")
