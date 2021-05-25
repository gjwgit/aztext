# -*- coding: utf-8 -*-
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@microsoft.com
#
# A command line script to analyze text.
#
# ml phrases aztext <sentence>
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

from mlhub.pkg import get_private

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

key, endpoint = get_private()

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
    response  = client.key_phrases(documents=documents)

    sep = ""
    for kp in response.documents:
        for p in kp.key_phrases:
            print(f"{sep}{p}", end="")
            sep = ","

# ------------------------------------------------------------------------
# Obtain text and analyze.
# ------------------------------------------------------------------------

txt = " ".join(args.sentence)

if txt != "":
    analyseText(txt)
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
