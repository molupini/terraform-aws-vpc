import requests
from os import environ
from os import getcwd
import fire
import json
import re


class HttpFetch(object):
    
    def ready(self, id):
        protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
        hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
        port = environ.get('IAC_ENDPOINT_PORT')
        url = f'{protocol}://{hostname}:{port}/resources/query/{id}'
        # debugging
        print(url)

        response = requests.get(url)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'resource ready, web {response.status_code}'}
            # print(err)
            raise Exception(err)

        deploy = response.json()['deployment']
        # print(deploy)
        if(deploy['stateDescription'] == 'ready'):
            return deploy['_id']
        else:
            raise Exception(1)

    def wsdir(self, id):
        pwd = getcwd().replace('/', '-')
        return f'{id}{pwd}'
 

    def destroy(self, id):
        protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
        hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
        port = environ.get('IAC_ENDPOINT_PORT')
        url = f'{protocol}://{hostname}:{port}/resources/query/{id}'
        # debugging
        # print(url)

        response = requests.get(url)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'resource destroy, web {response.status_code}'}
            # print(err)
            raise Exception(err)

        deploy = response.json()['deployment']
        # print(deploy)
        if(deploy['stateDescription'] == 'applyComplete'):
            return deploy['_id']
        else:
            raise Exception(1)

    # # TODO NEED TO VERIFY IF USER ACCOUNT THAT CONTROL FLAGS I.E. IS ADMIN IS HANDLED 
    # # TODO NEED TO VERIFY IF CAN COLLAPLES OTHER FUNCTION INTO THIS FUNC AS IT CARTERS FOR RESOURCES AND PARENT DOCUMENT TYPE
    # # REASON IS THAT BOTH TIMES REFERENCE RESOURCES IN RETURN DATA BELOW 
    def resources(self, id, res='', document='resources', element=''):
        protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
        hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
        port = environ.get('IAC_ENDPOINT_PORT')
        url = f'{protocol}://{hostname}:{port}/resources/query/{id}?document={document}'
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
            return json.dumps(deploy['resources'])
        else:
            raise 1

    def security(self, id, key='', res='', source_is='cidr'):
            protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
            hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
            port = environ.get('IAC_ENDPOINT_PORT')
            url = f'{protocol}://{hostname}:{port}/resources/query/{id}?document=security'
            # debugging
            # print(url)

            response = requests.get(url)
            if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
                err = {'error': f'resource security, web {response.status_code}'}
                # print(err)
                raise Exception(err)

            security = response.json()
            if security:
                if key == '':
                    try:
                        # return security['resources']
                        return json.dumps(security, separators=(',',':'), indent=2)
                    except:
                        err = {'error': f'resource, security not found'}
                        raise Exception(err)
                elif key == 'resources':
                    if res != '':
                        try:
                            # return security['resources']
                            return json.dumps(security['resources'][res], separators=(',',':'), indent=2)
                        except:
                            err = {'error': f'resource, security not found'}
                            raise Exception(err)
                    else:
                        try:
                            # return security['resources']
                            return json.dumps(security['resources'], separators=(',',':'), indent=2)
                        except:
                            err = {'error': f'resource, security not found'}
                            raise Exception(err)
                elif key == 'rules':
                    if res == '':
                        try:
                            # return security['resources']
                            return json.dumps(security['rules'], separators=(',',':'), indent=2)
                        except:
                            err = {'error': f'resource, security not found'}
                            raise Exception(err)
                    else:
                        i = 0
                        result = []
                        for sec in security['rules'][res]:
                            reg = False
                            if sec['forResource'] == res:
                                if source_is == 'cidr':
                                    reg = bool(re.match(r'^((\d{1,3}\.){3}\d{1,3}\/\d{1,2})$', sec['source']))
                                if source_is == 'sg':
                                    reg = bool(re.match(r'^(sg\-\w{15,34})$', sec['source']))
                            if reg:
                                result.append(sec)
                            i+=1
                # debugging
                # print(result)
                # return result
                # json.dumps(result)
                return json.dumps(result, separators=(',',':'), indent=2)
            else:
                raise 1

    def discovery(self, id, res=''):
        protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
        hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
        port = environ.get('IAC_ENDPOINT_PORT')
        url = f'{protocol}://{hostname}:{port}/resources/query/{id}?document=discovery'
        # debugging
        # print(url)

        response = requests.get(url)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'resource discovery, web {response.status_code}'}
            # print(err)
            raise Exception(err)

        deploy = response.json()
        if deploy:
            if res != '':
                try:
                    return json.dumps(deploy['resources'][res])
                except:
                    err = {'error': f'resource, discovery not found {res}'}
                    raise Exception(err)
            return json.dumps(deploy['resources'])
        else:
            raise 1

    def deploy(self, id):
        protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
        hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
        port = environ.get('IAC_ENDPOINT_PORT')
        url = f'{protocol}://{hostname}:{port}/resources/query/{id}?document=deployment'
        # debugging
        # print(url)

        response = requests.get(url)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'resource query, web {response.status_code}'}
            raise Exception(err)

        deploy = response.json()
        if deploy:
            return json.dumps(deploy['deployment'])
        else:
            raise 1
            
    def perimeter(self, id, element=''):
        protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
        hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
        port = environ.get('IAC_ENDPOINT_PORT')
        url = f'{protocol}://{hostname}:{port}/resources/query/{id}?document=perimeter'
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

    def tagging(self, id):
        protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
        hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
        port = environ.get('IAC_ENDPOINT_PORT')
        url = f'{protocol}://{hostname}:{port}/resources/query/{id}?document=tagging'
        # debugging
        # print(url)

        response = requests.get(url)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'resource tagging, web {response.status_code}'}
            # print(err)
            raise Exception(err)

        deploy = response.json()
        if deploy:
            return json.dumps(deploy['tagging'])
        else:
            raise 1

    # TODO NEED TO ASSIGN FUNCTION WITHIN TERRAFORM AWS VPC MODULE 
    def az(self, id, res='VPC'):
        protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
        hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
        port = environ.get('IAC_ENDPOINT_PORT')
        url = f'{protocol}://{hostname}:{port}/resources/query/{id}?document=resources'
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
                    return json.dumps(deploy['resources'][res])
                except:
                    err = {'error': f'resource, resources not found {res}'}
                    raise Exception(err)
            return json.dumps(deploy['resources'])
        else:
            raise 1

    def status(self, id):
            protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
            hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
            port = environ.get('IAC_ENDPOINT_PORT')
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

    def seedOne(self, id):
        protocol = environ.get('IAC_ENDPOINT_PROTOCOL')
        hostname = environ.get('IAC_ENDPOINT_HOSTNAME')
        port = environ.get('IAC_ENDPOINT_PORT')
        url = f'{protocol}://{hostname}:{port}/resources/update/{id}'
        l = 0
        r = 0
        data = None
        # debugging
        # print(url)
        try:
            file = open(f'./{id}-output.json', 'r').read()
            # print(file)
            load = json.loads(file)
            try:
                l = load['logicalId']['value']
                r = load['resourceType']['value']
                # n = load['logicalName']['value']
                if (len(l) > 0):
                    # inf = {'info': f'{id}, logicalId={l}'}
                    # print(inf)
                    # inf = {'info': f'{id}, resourceType={r}'}
                    # print(inf)
                    data = {
                        "logicalId": l,
                        "resourceType": r
                    }
                    
            except KeyError as ke:
                err = {'error': f'{id}, KeyError {ke}'}
                print(err)
                return 1
        except FileNotFoundError as fe:
            err = {'error': f'{id}, FileNotFoundError {fe}'}
            print(err)
            return 1
        # print(url)
        print(data)
        response = requests.patch(url, json=data)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202:
            err = {'error': f'resource seed, web {response.status_code}'}
            raise Exception(err)
        return 0

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