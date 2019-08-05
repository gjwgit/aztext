# -*- coding: utf-8 -*-
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@microsoft.com
#
# A command line script to analyze text.
#
# ml analyze aztext <sentence>
# 
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python
#

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

import sys
import os
import pickle
import requests
import argparse

from textwrap import fill
from pprint import pprint

from mlhub.pkg import azkey

# Defaults.

SERVICE = "Text Analytics"
KEY_FILE  = os.path.join(os.getcwd(), "private.txt")

# ----------------------------------------------------------------------
# Parse command line arguments
# ----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'sentence',
    nargs="*",
    help='sentence to analyse')

args = option_parser.parse_args()

# ----------------------------------------------------------------------
# Request subscription key and endpoint from user.
# ----------------------------------------------------------------------

key, endpoint = azkey(KEY_FILE, SERVICE, verbose=False)

def analyseText(txt):
    documents = { 'documents': [{ 'id': '1', 'text': txt }]}
    url       = endpoint + "languages"
    headers   = {"Ocp-Apim-Subscription-Key": key}
    response  = requests.post(url, headers=headers, json=documents)
    languages = response.json()

    l    = languages['documents'][0]
    dl   = l['detectedLanguages'][0]
    lang = dl['iso6391Name']

    print(f"{dl['score']},{lang},", end="")

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

    url         = endpoint + "keyPhrases"
    headers     = {'Ocp-Apim-Subscription-Key': key}
    response    = requests.post(url, headers=headers, json=documents)
    key_phrases = response.json()

    sep = ""
    for kp in key_phrases['documents']:
        for p in kp['keyPhrases']:
            print(f"{sep}{p}", end="")
            sep = ":"
    print(",", end="")
    
    url      = endpoint + "entities"
    headers  = {"Ocp-Apim-Subscription-Key": key}
    response = requests.post(url, headers=headers, json=documents)
    entities = response.json()

    for es in entities['documents']:
        sep = ""
        for e in es['entities']:
            print(f"{sep}{e['name']}", end="") # e['wikipediaUrl']
            sep=":"

# Obtain text and analyze.

txt = " ".join(args.sentence)

if txt == "":

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
