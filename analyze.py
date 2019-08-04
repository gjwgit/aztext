# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# This demo is based on the Azure Cognitive Services Text Analytics
# Quick Starts:
# 
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python
#

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
import argparse

from textwrap import fill
from pprint import pprint

# ----------------------------------------------------------------------
# Parse command line arguments
# ----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'sentence',
    nargs="?",
    help='sentence to analyse')

args = option_parser.parse_args()

# ----------------------------------------------------------------------

# TODO move to using mlhub.pkg
#
# Prompt the user for the key and region and save into private.py for
# future runs of the model. The contents of that file is:
#
# subscription_key = "a14d...ef24"
# assert subscription_key
# region = "southeastasia"

if os.path.isfile(fname):
    exec(open(fname).read())
else:
    print("""An Azure resource is required to access the Azure Text Analytics service.
See the README for details of a free subscription. Then provide the key and 
region information here.
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

def analyseText(txt):
    documents = { 'documents': [{ 'id': '1', 'text': txt }]}

    language_api_url = text_analytics_base_url + "languages"
    headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
    response  = requests.post(language_api_url, headers=headers, json=documents)
    languages = response.json()

    l  = languages['documents'][0]
    dl = l['detectedLanguages'][0]
    lang = dl['iso6391Name']

    documents = { 'documents': [{ 'id': '1', 'language': lang, 'text': txt }]}

    print(f"{dl['score']},{lang},", end="")

    sentiment_api_url = text_analytics_base_url + "sentiment"
    headers    = {"Ocp-Apim-Subscription-Key": subscription_key}
    response   = requests.post(sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()

    # Notice id is not a supported language for the following.

    sep = ""
    for s in sentiments['documents']:
        print(f"{sep}{s['score']:0.2f}", end="")
        sep=":"
    print(",", end="")

    key_phrase_api_url = text_analytics_base_url + "keyPhrases"
    headers     = {'Ocp-Apim-Subscription-Key': subscription_key}
    response    = requests.post(key_phrase_api_url, headers=headers, json=documents)
    key_phrases = response.json()

    sep = ""
    for kp in key_phrases['documents']:
        for p in kp['keyPhrases']:
            print(f"{sep}{p}", end="")
            sep = ":"
    print(",", end="")
    
    entity_linking_api_url = text_analytics_base_url + "entities"
    headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
    response  = requests.post(entity_linking_api_url, headers=headers, json=documents)
    entities = response.json()

    for es in entities['documents']:
        sep = ""
        for e in es['entities']:
            print(f"{sep}{e['name']}", end="") # e['wikipediaUrl']
            sep=":"


txt = args.sentence

if txt is None:

    prompt = "Enter text to be analysed\nQuit with Ctrl-d, Output conf,lang,sentiment,phrases,entities):\n> "

    try:
        txt = input(prompt)
    except EOFError:
        print()
        sys.exit(0)

    while txt != '':

        analyseText(txt)

        try:
            print()
            txt = input(prompt)
        except EOFError:
            print()
            sys.exit(0)
else:
    analyseText(txt)
    print()
