#!/usr/bin/env python

# Copyright 2016 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Analyzes text using the Google Cloud Natural Language API."""

import argparse
import json
import sys
import pandas as pd

import googleapiclient.discovery


def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'


def analyze_entities(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding,
    }

    service = googleapiclient.discovery.build('language', 'v1')

    request = service.documents().analyzeEntities(body=body)
    response = request.execute()

    return response


def analyze_sentiment(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
            'language': 'EN',
        },
        'encoding_type': encoding
    }

    service = googleapiclient.discovery.build('language', 'v1')

    request = service.documents().analyzeSentiment(body=body)
    response = request.execute()

    return response


def analyze_syntax(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding
    }

    service = googleapiclient.discovery.build('language', 'v1')

    request = service.documents().analyzeSyntax(body=body)
    response = request.execute()

    return response

data = pd.read_csv('data.csv')

counter = 0
def sentiment(article): 
    sentiment.counter += 1 
    print(sentiment.counter)
    return analyze_sentiment(article)['documentSentiment']['score']
sentiment.counter = 0 


import time
start_time = time.time()
print(analyze_sentiment(data['headline'].values[0])['documentSentiment']['score'])
print("--- %s seconds ---" % (time.time() - start_time))


#from concurrent.futures.process import ProcessPoolExecutor
#from concurrent.futures import wait
#from concurrent.futures import as_completed


#start_time = time.time()
#executor = ProcessPoolExecutor(8)
#futures = [executor.submit(sentiment, item) for item in data['headline'].values[:900]]
#wait(futures)
#print("--- %s seconds ---" % (time.time() - start_time))

#results = []
#for future in as_completed(futures):
#    try: 
#        results += [future.result()]
#    except:
#        results += [None]


#pd.DataFrame(results).to_csv('1.csv')

data['sentiment'] = data['headline'].apply(sentiment)

data.to_csv('new_data.csv')

