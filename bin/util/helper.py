import requests
from os import environ
from os import getcwd
import fire
import json
import re


class HttpFetch(object):
    
    def resources(self, id, res='', document='resources', element='', link=''):
        if link == '':
            protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
            hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
            port = environ.get('IAC_ENDPOINT_PORT')
            uri = f'{protocol}://{hostname}:{port}'
        else:
            uri = f'{link}'
        url = f'{uri}/resources/query/{id}?document={document}'
        # debugging
        # print(url)

        response = requests.get(url)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'resource resources, web {response.status_code}'}
            # print(err)
            raise Exception(err)

        deploy = response.json()
        if deploy:
            if res != '':
                try:
                    if element != '':
                        # print(element)
                        try:
                            return deploy['resources'][res][element]
                        except:
                            return 0
                    return json.dumps(deploy['resources'][res])
                except:
                    err = {'error': f'resource, resources not found {res}'}
                    raise Exception(err)
            return json.dumps(deploy['resources'], separators=(',',':'), indent=2)
        else:
            raise 1

    def tagging(self, id, link=''):
        if link == '':
            protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
            hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
            port = environ.get('IAC_ENDPOINT_PORT')
            uri = f'{protocol}://{hostname}:{port}'
        else:
            uri = f'{link}'
        url = f'{uri}/resources/query/{id}?document=tagging'
        # debugging
        # print(url)

        response = requests.get(url)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'resource tagging, web {response.status_code}'}
            # print(err)
            raise Exception(err)

        deploy = response.json()
        if deploy:
            return json.dumps(deploy['tagging'], separators=(',',':'), indent=2)
        else:
            raise 1


if __name__ == '__main__':
    fire.Fire(HttpFetch)