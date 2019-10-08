# -*- coding: utf-8 -*-
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@microsoft.com
#
# A command line script to list supported languages.
#
# ml sypported aztext
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
import requests

from bs4 import BeautifulSoup
from mlhub.pkg import azkey, mlcat

# ----------------------------------------------------------------------
# Parse command line arguments
# ----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'language',
    nargs="?",
    help='a language code to check')

option_parser.add_argument(
    '--header',
    action='store_true')

args = option_parser.parse_args()

# ------------------------------------------------------------------------
# Obtain meta data about supported languages.
# ------------------------------------------------------------------------
#
# According to 
#
# https://docs.microsoft.com/en-gb/azure/cognitive-services/
# text-analytics/language-support
#
# the list of supported languages is not published.
#
# Visit the above page to review the manual list.

url = "https://docs.microsoft.com/en-gb/azure/cognitive-services/" +\
      "text-analytics/language-support"

response = requests.get(url, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find_all('table')[0]
rows = table.select('tbody > tr')
header = [th.text.rstrip() for th in table.find_all('th')]

if args.header: print("language,code,sentiment,phrases,entity")
for row in rows:
    td = row.find_all("td")
    lang = td[0].text.rstrip()
    code = td[1].text.rstrip()
    if args.language == None or args.language in code:
        sentiment = len(td[2].text.rstrip()) > 0
        phrases   = len(td[3].text.rstrip()) > 0
        entity    = len(td[4].text.rstrip()) > 0
        print(f"{lang},{code},{sentiment},{phrases},{entity}")
