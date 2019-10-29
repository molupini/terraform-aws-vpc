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

    def state(self, id, res = ''):
        protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
        hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
        port = environ.get('IAC_ENDPOINT_PORT')
        url = f'{protocol}://{hostname}:{port}/resources/query/{id}?document=state'
        # debugging
        # print(url)

        response = requests.get(url)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'resource query state, web {response.status_code}'}
            # print(err)
            raise Exception(err)
        states = response.json()
        try:
            if states[res]:
                return states[res]
        except KeyError as ke:
            err = {'error': f'{id}, state keyError'}
            print(err)
            raise KeyError(ke)

    def wsdir(self, id):
        pwd = getcwd().replace('/', '-')
        return f'{id}{pwd}'
 
    # TODO SEED MANY FUNC, FOR LOGICAL ID UPDATING, KEY IS THE RESOURCE ID WITHIN TERRAFORM, DES IS THE DESTINATION KEY ON THE API, RES IS THE RESOURCE ID ON THE API
    def seedMany(self, deployId, key='', apiKey='', resId=''):
        protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
        hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
        port = environ.get('IAC_ENDPOINT_PORT')
        # API URL
        url = f'{protocol}://{hostname}:{port}/resources/update/'
        k = 0
        ak = 0
        ids = 0
        data = None
        # debugging
        # print(url)
        try:
            # DEPLOYMENT ID FOR SPECIFIC FILE 
            file = open(f'./{deployId}-output.json', 'r').read()
            load = json.loads(file)
            # TRY MATCH KEYS WITH JSON FILE
            try:
                # TERRAFORM FILE KEY 
                k = load[key]['value']
                # API TARGET KEY 
                ak = apiKey
                # THE ITERATOR 
                ids = load[resId]['value']
                if (len(k) > 0):
                    data = {
                        ak: k
                    }
            except KeyError as ke:
                err = {'error': f'{id}, KeyError {ke}'}
                print(err)
                return 1
        except FileNotFoundError as fe:
            err = {'error': f'{id}, FileNotFoundError {fe}'}
            print(err)
            return 1
        # THE ITERATOR 
        array = ids.split(';')
        if array:
            for a in array:
                i = a
                d = data[ak][a]
                # debugging
                # print(i)
                # print(d)
                response = requests.patch(f'{url}{i}', json={ak: d})
            if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
                err = {'error': f'resource seed, web {response.status_code}'}
                raise Exception(err)
            return 0
        else:
            return 1
 


if __name__ == '__main__':
    fire.Fire(HttpFetch)