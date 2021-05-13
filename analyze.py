# -*- coding: utf-8 -*-
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@microsoft.com
#
# A command line script to analyze text.
#
# ml analyze aztext [<sentence>]
# 
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/
#   quickstarts/python-sdk
#

# ----------------------------------------------------------------------
# Import the required libraries.
# ----------------------------------------------------------------------

import sys
import os
import argparse

from mlhub.utils import get_private

# pip3 install --upgrade --user azure-cognitiveservices-language-textanalytics

from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

# ----------------------------------------------------------------------
# Parse command line arguments: sentence
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
PRIVATE_FILE = "private.json"

path = os.path.join(os.getcwd(), PRIVATE_FILE)

private_dic = get_private(path, "aztext")

if "key" not in private_dic["Text Analytics"]:
    print("There is no key in private.json. Please run ml configure aztext to upload your key.", file=sys.stderr)
    sys.exit(1)

key = private_dic["Text Analytics"]["key"]

endpoint = private_dic["Text Analytics"]["endpoint"]

credentials = CognitiveServicesCredentials(key)
client = TextAnalyticsClient(endpoint=endpoint, credentials=credentials)


# ------------------------------------------------------------------------
# Helper function.
# ------------------------------------------------------------------------

def analyseText(txt):
    documents = [{'id': '1', 'text': txt}]
    response = client.detect_language(documents=documents)

    l = response.documents[0]
    dl = l.detected_languages[0]
    lang = dl.iso6391_name

    print(f"{dl.score},{lang},", end="")

    documents = [{'id': '1', 'language': lang, 'text': txt}]
    response = client.sentiment(documents=documents)

    sep = ""
    for s in response.documents:
        print(f"{sep}{s.score:0.2f}", end="")
        sep = ":"
    print(",", end="")

    response = client.key_phrases(documents=documents)

    sep = ""
    for kp in response.documents:
        for p in kp.key_phrases:
            print(f"{sep}{p}", end="")
            sep = ":"
    print(",", end="")

    response = client.entities(documents=documents)

    for es in response.documents:
        sep = ""
        for e in es.entities:
            print(f"{sep}{e.type}={e.name}", end="")  # e['wikipediaUrl']
            sep = ":"


# ------------------------------------------------------------------------
# Analyse sentence obtained from command line, pipe, or interactively.
# ------------------------------------------------------------------------

txt = " ".join(args.sentence)

if txt != "":
    analyseText(txt)
    print()
elif sys.stdin.isatty():
    for txt in sys.stdin.readlines():
        analyseText(txt)
        print()
else:
    print("Enter text to be analysed. Quit with Empty or Ctrl-d.\n" + \
          "(Output: conf,lang,sentiment,phrases,entities)\n")
    prompt = '> '
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
