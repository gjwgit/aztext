# -*- coding: utf-8 -*-
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@microsoft.com
#
# A command line script to analyze text.
#
# ml sentiment aztext <sentence>
# 
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/
#   quickstarts/python-sdk
#

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

import sys
import argparse

from utils import request_priv_info

# pip3 install --upgrade --user azure-cognitiveservices-language-textanalytics

from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

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

key, endpoint = request_priv_info()

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
    response  = client.sentiment(documents=documents)

    sep = ""
    for s in response.documents:
        z = (s.score-0.5)/0.5
        print(f"{z:0.2f}", end="")
        sep=":"

# ------------------------------------------------------------------------
# Obtain text and analyze.
# ------------------------------------------------------------------------

txt = " ".join(args.sentence)

if txt != "":
    analyseText(txt)
    print()
elif not sys.stdin.isatty():
    for txt in sys.stdin.readlines():
        analyseText(txt)
        print()
else:
    print("Enter text to be analysed. Quit with Empty or Ctrl-d.\n")
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
