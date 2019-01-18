# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# This demo is based on the Azure Cognitive Services Text Analytics Quick Starts
# 
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python
#

print("""================================
Interactive Azure Text Analytics
================================

Welcome to MLHub's demonstration scorer for the pre-built 
Text Analytics model from Azure's Cognitive Services.
""")

# Defaults.

KEY_FILE = "private.py"
DEFAULT_REGION = "southeastasia"
CANNED_PKL = "canned.pkl"

fname = KEY_FILE
region = DEFAULT_REGION
subscription_key = None
live = True

# Import the required libraries.

import sys
import os
import pickle
import requests
from textwrap import fill
from pprint import pprint

# Prompt the user for the key and region and save into private.py for
# future runs of the model. The contents of that file is:
#
# subscription_key = "a14d...ef24"
# assert subscription_key
# region = "southeastasia"

if os.path.isfile(fname):
    print("""The following file was found and is assumed to contain an
Azure Text Analytics subscription key and region. We will
load the file and use this information.

""" + os.getcwd() + "/" + fname)
    exec(open(fname).read())
else:
    print("""An Azure resource is required to access this service (and to run this
score demo). See the README for details of a free subscription. Then you can
provide the key and the region information here.
""")
    sys.stdout.write("Please enter your Text Analytics subscription key []: ")
    subscription_key = input()

    sys.stdout.write("Please enter your region [southeastasia]: ")
    region = input()
    if len(region) == 0: region = DEFAULT_REGION

    if len(subscription_key) > 0:
        assert subscription_key

cognitive_services_url = "https://" + region + ".api.cognitive.microsoft.com"
text_analytics_base_url = cognitive_services_url + "/text/analytics/v2.0/"

prompt = "\nEnter text to be analysed (Quit by Ctrl-d):\n> "
try:
    txt = input(prompt)
except EOFError:
    print()
    sys.exit(0)

while txt != '':

    print("")
    print(fill(txt))
    print("")
    
    documents = { 'documents': [{ 'id': '1', 'text': txt }]}

    language_api_url = text_analytics_base_url + "languages"
    headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
    response  = requests.post(language_api_url, headers=headers, json=documents)
    languages = response.json()

    l  = languages['documents'][0]
    dl = l['detectedLanguages'][0]
    lang = dl['iso6391Name']
    print("This is {} ({}) with score of {}.".format(dl['name'], lang, dl['score']))

    documents = { 'documents': [{ 'id': '1', 'language': lang, 'text': txt }]}

    sentiment_api_url = text_analytics_base_url + "sentiment"
    headers    = {"Ocp-Apim-Subscription-Key": subscription_key}
    response   = requests.post(sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()

    # Notice id is not a supported language for the following.
    
    for s in sentiments['documents']:
        print("This has a sentiment rating of {0:.2f}.".format(s['score']))

    key_phrase_api_url = text_analytics_base_url + "keyPhrases"
    headers     = {'Ocp-Apim-Subscription-Key': subscription_key}
    response    = requests.post(key_phrase_api_url, headers=headers, json=documents)
    key_phrases = response.json()

    for kp in key_phrases['documents']:
        print("The key phrases are: {}.".format(kp['keyPhrases']))

    entity_linking_api_url = text_analytics_base_url + "entities"
    headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
    response  = requests.post(entity_linking_api_url, headers=headers, json=documents)
    entities = response.json()

    for es in entities['documents']:
        print("Entities:")
        for e in es['entities']:
            print("  {}:\t{}.".format(e['name'], e['wikipediaUrl']))

    try:
        txt = input(prompt)
    except EOFError:
        print()
        sys.exit(0)
