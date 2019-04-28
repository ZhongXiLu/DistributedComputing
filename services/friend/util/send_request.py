import requests
from requests.exceptions import RequestException


class ResponseObj:
    def __init__(self, response, json, status_code):
        self.response = response
        self.json = json
        self.status_code = status_code


def send_request(method: str, service: str, route: str, **kwargs):
    func = getattr(requests, method.lower())
    try:
        response = func(f'http://{service}:5000/{route}', **kwargs)
        if response:
            response_object = ResponseObj(response, response.json(), response.status_code)
        else:
            response_object = ResponseObj(response, None, response.status_code)
    except RequestException as e:
        response_json = {'status': 'fail', 'message': f'{service} service down.', 'error_type': e.__class__.__name__}
        response_object = ResponseObj(None, response_json, 503)
    return response_object
