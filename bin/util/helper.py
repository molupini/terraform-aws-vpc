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
                    # RETURN EMPTY ARRAY TO PREVENT RESOURCE USAGE WITH COUNT PARAM
                    err = {'error': f'resource, resources not found {res}'}
                    empty = json.dumps([])
                    return empty
            return json.dumps(deploy['resources'], separators=(',',':'), indent=2)
        else:
            return 1

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

    def status(self, id, code=0, app='null', link='null'):
            if link == 'null':
                protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
                hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
                port = environ.get('IAC_ENDPOINT_PORT')
                uri = f'{protocol}://{hostname}:{port}'
            else:
                uri = f'{link}'
            url = f'/resources/query/{id}?document=tagging'
            # debugging
            # print(url)
            try:
                if app == 'state':
                    url = f'{uri}/resources/status/{id}?state={code}&application={app}'
                else:
                    url = f'{uri}/resources/status/{id}?state={code}'
                response = requests.get(url)
                if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
                    err = {'error': f'resource state, web {response.status_code}'}
                    raise Exception(err)
                return 0
            except:
                return 1

    def state(self, id, res='null', link='null'):
        
        if link == 'null':
            protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
            hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
            port = environ.get('IAC_ENDPOINT_PORT')
            uri = f'{protocol}://{hostname}:{port}'
        else:
            uri = f'{link}'
        
        url = f'{uri}/resources/query/{id}?document=state'
        response = requests.get(url)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'resource query state, web {response.status_code}'}
            raise Exception(err)
        states = response.json()
        try:
            if res == 'null':
                return json.dumps(states, separators=(',',':'), indent=2)
            else:
                if states[res]:
                    return states[res]
        except KeyError as ke:
            err = {'error': f'{id}, state keyError'}
            raise KeyError(ke)
        return 1

    def perimeter(self, id, element='', link='null'):
        if link == 'null':
            protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
            hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
            port = environ.get('IAC_ENDPOINT_PORT')
            uri = f'{protocol}://{hostname}:{port}'
        else:
            uri = f'{link}'
        url = f'{uri}/resources/query/{id}?document=perimeter'
        # debugging
        # print(url)
        response = requests.get(url)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'perimeter query, web {response.status_code}'}
            raise Exception(err)

        perimeter = response.json()
        if element != '':
            try:
                return json.dumps(perimeter['perimeter'][element])
            except KeyError as ke:
                return json.dumps(perimeter['perimeter']['default'])
        elif perimeter:
            return json.dumps(perimeter['perimeter'])
        else:
            raise 1

    # TODO SEED MANY FUNC, FOR LOGICAL ID UPDATING, KEY IS THE RESOURCE ID WITHIN TERRAFORM, DES IS THE DESTINATION KEY ON THE API, RES IS THE RESOURCE ID ON THE API
    def seedMany(self, deployId, key='', apiKey='', resId='', link='null'):
        if link == 'null':
            protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
            hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
            port = environ.get('IAC_ENDPOINT_PORT')
            uri = f'{protocol}://{hostname}:{port}'
        else:
            uri = f'{link}'
        # API URL
        url = f'{uri}/resources/update/'
        k = 0
        ak = 0
        ids = 0
        data = None
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
        # debugging
        # print("data =")
        # print(data)
        # print("ids =")
        # print(ids)
        # print("url =")
        # print(url)
        array = ids.split(';')
        # debugging
        # print("array =")
        # print(array)
        if array:
            for a in array:
                i = a
                d = data[ak][a]
                # debugging
                # print("array loop =")
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