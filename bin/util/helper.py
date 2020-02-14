import requests
from os import environ
from os import getcwd
import fire
import json
import re

protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
port = environ.get('IAC_ENDPOINT_PORT')
uri = f'{protocol}://{hostname}:{port}'


class HttpFetch(object):

    # APP
    # FETCH TAG, DEPLOYMENT, CONFIG, CONNECTOR ETC 
    def app(self, id, document='tag', res='null'):
        # WEB REQUEST
        url = f'{uri}/app{id}?document={document}'
        response = requests.get(url)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'web {response.status_code}'}
            raise Exception(err)
        # TO JSON
        deploy = response.json()
        if deploy:
            if res != 'null':
                try:
                    return json.dumps(deploy[res], separators=(',',':'), indent=2)
                except:
                    # RETURN EMPTY ARRAY TO PREVENT RESOURCE USAGE WITH COUNT PARAM
                    err = {'error': f'not found {res}'}
                    empty = json.dumps([])
                    return empty
            return json.dumps(deploy, separators=(',',':'), indent=2)
        else:
            return 1

    # STATUS
    # SET STATUS OF DEPLOYMENT WITH SPECIFIC CONTROL STAGES 
    def status(self, id, code=0):
            url = f'{uri}/app/deployment{id}?state={code}'
            try:
                response = requests.get(url)
                if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
                    err = {'error': f'resource state, web {response.status_code}'}
                    raise Exception(err)
                return 0
            except:
                return 1

    # ABBR
    # MATCHING DESCRIPTION
    # KEY, PERIMETER 
    # CONDITIONAL FOR DESCRIPTION EXAMPLE public
    # RETURN SPECIFIC ELEMENT SEE DEFAULT, ELSE OBJECT
    # ABBR NOT BE TREATED AS CONFIG
    def abbr(self, key='null', description='null', element = 'elementLabel'):
        try:
            url = f'{uri}/svc/abbr?key={key}'
            response = requests.get(url)
            if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
                err = {'error': f'web {response.status_code}'}
                raise Exception(err)
            # TO JSON
            abbr = response.json()
            if key != 'null':
                for a in abbr:
                    if a['description'] == description:
                        # debugging
                        # print('a =')
                        # print(a)
                        return a['elementLabel']
                return abbr
            return 1
        except:
            return 1

    # DISCOVERY
    # ELEMENT EXAMPLE Name
    # ARGS EXAMPLE resourceType=s3 application=tfsta leafOrganization=sgti environment=pst state=6
    # RETURN SPECIFIC ELEMENT EXAMPLE name
    def discovery(self, id, resourceType='s3', element='null', *args):
        # LABEL
        # GET LABEL AND BUILD QUERY
        label = f'{uri}/svc/label?resourceType={resourceType}'
        response = requests.get(label)
        js = response.json()
        key = js['keyMap']
        # print(key)

        # TAG
        # GET TAG FOR RESOURCE BEING DEPLOYED AND SELECT KEYS THAT ARE PRESENT
        main = HttpFetch
        tag = main.app(self, id)
        js = json.loads(tag)
        # BUILD QUERY STRING WITH ARGS
        array = []
        # USE LABEL AND KEY FROM ABOVE TO APPEND ARRAY
        for t in js:
            for k in key:
                value = js[t][0][k]
                # EXCLUDE PARAM AS REQUIRED BY QUERY STRING
                if k != 'resourceType':
                    array.append(f'{k}={value}')
        # AMEND ARRAY AND ARGS 
        if len(list(args)) > 0:
            array = array + list(args)
        # QUERY STRING
        string = '&'.join(array)

        # CONNECTOR 
        # TODO NOT NECESSARY WITHIN QUERY STRING
        # connector = f'{uri}/app{id}?document=connector'
        # response = requests.get(connector)
        # js = response.json()
        # con = js['_id']

        # DISCOVERY 
        # BETWEEN ? ARRAY JOIN FROM ABOVE WITH ARGS AND STATE
        discovery = f'{uri}/app/tag/discovery?resourceType={resourceType}&{string}'
        response = requests.get(discovery)

        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'web {response.status_code}'}
            raise Exception(err)

        # TO JSON
        js = response.json()
        # print(js)
        try:
            return js[element]
        except:
            return json.dumps(js, separators=(',',':'), indent=2)
        return 1

    # OPEN FILE
    # DEPLOYMENT ID FOR SPECIFIC FILE 
    def openFile(self, id):
        try:
            with open(f'./{id}-output.json', 'r') as f:
                load = f.read()
                return json.loads(load)
        except:
            return 1
        finally:
            f.close()

    # SEED 
    # ID, DEPLOYMENT ID
    # KEY, WITHIN FILE
    # API KEY, WEB SERVICE KEY 
    # RES ID, RESOURCE ID
    def seed(self, id, document='resource', key='', apiKey=''):
        
        try:
            # DEPLOYMENT ID FOR SPECIFIC FILE 
            main = HttpFetch
            load = main.openFile(self, id)
            # TRY MATCH KEYS WITH JSON FILE
            try:
                # TERRAFORM FILE KEY 
                load = load[key]['value']
            except KeyError as ke:
                err = {'error': f'{id}, KeyError {ke}'}
                print(err)
                return 1
            # debugging
            # print('load=')
            # print(load)
            # UPDATE DOCUMENT
            # BUILD BODY WITH API KEY 
            # USE THE DEPLOYMENT ID TO SERVE THE WHOLE DEPLOYMENT 
            # USE THE ID WITHIN LOAD AS THE ID AND THE VALUE WILL BE ADDED THE BODY WITH THE API KEY PARAM
            for key in load:
                url = f'{uri}/app{key}?document={document}'
                # debugging
                # print('url =')
                # print(url)
                body = {apiKey: load[key]}
                # debugging
                # print('body =')
                # print(body)
                response = requests.patch(url, json=body)
                if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
                    err = {'error': f'web {response.status_code}'}
                    raise Exception(err)
                return 0
        except Exception as e:
            print(e)
            return 1
 

if __name__ == '__main__':
    fire.Fire(HttpFetch)