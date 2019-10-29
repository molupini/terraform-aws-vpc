import requests
from os import environ
from os import getcwd
import fire
import json
import re


class HttpFetch(object):
    
    def resources(self, id, res='null', document='resources', element='null', link='null'):
        if link == 'null':
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
            if res != 'null':
                try:
                    if element != 'null':
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

    def tagging(self, id, link='null'):
        if link == 'null':
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

    def status(self, id, link='null'):
            if link == 'null':
                protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
                hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
                port = environ.get('IAC_ENDPOINT_PORT')
                uri = f'{protocol}://{hostname}:{port}'
            else:
                uri = f'{link}'
            url = f'{uri}/resources/query/{id}?document=tagging'
            n = 0
            d = 0
            # debugging
            # print(url)
            try:
                file = open(f'./{id}-output.json', 'r').read()
                print(file)
                load = json.loads(file)
                try:
                    d = load['done']['value']
                    a = load['application']['value']
                    if (d == 0):
                        inf = {'info': f'{id}, done={d}'}
                        print(inf)
                        n = 6
                        url = f'{protocol}://{hostname}:{port}/resources/status/{id}?state={n}&application={a}'
                except KeyError as ke:
                    err = {'error': f'{id}, KeyError {ke}'}
                    print(err)
                    n = 8
                    url = f'{protocol}://{hostname}:{port}/resources/status/{id}?state={n}'
            except FileNotFoundError as fe:
                err = {'error': f'{id}, FileNotFoundError {fe}'}
                print(err)
                n = 10
                url = f'{protocol}://{hostname}:{port}/resources/status/{id}?state={n}'
            response = requests.get(url)
            if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
                err = {'error': f'resource state, web {response.status_code}'}
                raise Exception(err)
            return 0


if __name__ == '__main__':
    fire.Fire(HttpFetch)