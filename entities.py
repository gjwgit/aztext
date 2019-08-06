# -*- coding: utf-8 -*-
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@microsoft.com
#
# A command line script to analyze text.
#
# ml analyze entities <sentence>
# 
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/
#   quickstarts/python-sdk
#

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

import sys
import os
import argparse

from mlhub.pkg import azkey

# pip3 install --upgrade --user azure-cognitiveservices-language-textanalytics

from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

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

key, endpoint = azkey(KEY_FILE, SERVICE, verbose=False, baseurl=True)
credentials   = CognitiveServicesCredentials(key)
client        = TextAnalyticsClient(endpoint=endpoint, credentials=credentials)

# ------------------------------------------------------------------------
# Helper function
# ------------------------------------------------------------------------

def analyseText(txt):
    documents = [{ 'id': '1', 'text': txt }]
    response  = client.detect_language(documents=documents)

    l    = response.documents[0]
    dl   = l.detected_languages[0]
    lang = dl.iso6391_name

    documents = [{ 'id': '1', 'language': lang, 'text': txt }]
    response  = client.entities(documents=documents)

    for es in response.documents:
        sep = ""
        for e in es.entities:
            print(f"{sep}{e.type}={e.name}", end="") # e['wikipediaUrl']
            sep=","

# ------------------------------------------------------------------------
# Obtain text and analyze.
# ------------------------------------------------------------------------

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
