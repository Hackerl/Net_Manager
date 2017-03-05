import requests

rsp = requests.post('http://127.0.0.1/update', data={
            'name': 'neteasy',
            'version': '2.0'

        })
