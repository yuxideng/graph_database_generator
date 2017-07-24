# -*- coding: utf-8 -*-
import argparse
import json
import os
from rosette.api import API, DocumentParameters, RosetteException
import def14a_download

def run_relation(relationships_text_data,key, altUrl='https://api.rosette.com/rest/v1/'):
    # Create an API instance
    api = API(user_key=key, service_url=altUrl)
   # relationships_text_data = "Tim has served as director of Apple Inc for 8 years. Before, he worked in Tesla"
    params = DocumentParameters()
    params["content"] = relationships_text_data
    api.set_option('accuracyMode', 'PRECISION')
    try:
        return api.relationships(params)
    except RosetteException as e:
        print(e)

def run_entities(entities_text_data,key,altUrl='https://api.rosette.com/rest/v1/'):
    # Create an API instance
    api = API(user_key=key, service_url=altUrl)
    #entities_text_data = "Tim has served as the director of Apple Inc in 2010"
    params = DocumentParameters()
    params["content"] = entities_text_data
    params["genre"] = "social-media"
    try:
        return api.entities(params)
    except RosetteException as e:
        print(e)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Calls the ' + os.path.splitext(os.path.basename(__file__))[
                                         0] + ' endpoint')
    parser.add_argument('-k', '--key', help='Rosette API Key', required=True)
    parser.add_argument('-u', '--url', help="Alternative API URL", default='https://api.rosette.com/rest/v1/')
    parser.add_argument('-f', '--file', help="data.txt file", required=True)
    args = parser.parse_args()
    def14a_download.get_filings(args.file,args.key,args.url)