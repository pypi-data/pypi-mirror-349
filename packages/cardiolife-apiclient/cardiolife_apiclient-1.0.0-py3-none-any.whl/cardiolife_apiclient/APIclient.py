import requests
import base64
import numpy as np
from collections.abc import Iterable

def sync_request(url, method='POST', headers=None, payload=None):
    """Simple sync request using requests."""
    headers = headers or {}
    method = method.upper()
    if method == 'GET':
        resp = requests.get(url, headers=headers, params=payload)
    else:
        resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()

def is_array(o):
    """Check if object is array-like (list, tuple, ndarray)."""
    return isinstance(o, (list, tuple, np.ndarray))

def is_iter(o):
    """Check if object is an iterable (excluding strings and bytes)."""
    return isinstance(o, Iterable) and not isinstance(o, (str, bytes, dict))

def listify(o):
    """ Transforms input into a list. """
    if o is None: return []
    if isinstance(o, list) or is_array(o): return o
    if type(o)==np.ndarray: return list(o)
    if isinstance(o, str): return [o]
    if isinstance(o, dict): return [o]
    if is_iter(o): return list(o)
    return [o]

def base64_encode(data):
    """
    Base64 encode data, that can be either a binary blob (bytes) or a string.
    Returns the base64-encoded string of the input data.
    """
    # If data is a string, convert it to bytes
    if isinstance(data, str): data = data.encode('utf-8')
    # Base64 encode the bytes
    return base64.b64encode(data).decode('utf-8')


class APIClient:
    def __init__(self, key: str, url: str):
        self.key = key
        self.url = url.rstrip('/')

    def do_request(self, route: str, payload: dict):
        headers = {'Authorization': f'Bearer {self.key}'}
        method = 'GET' if route == '/apiserver/check' else 'POST'
        return sync_request(f'{self.url}{route}', method=method, headers=headers, payload=payload)

    def get_signed_urls(self, fnames):
        return self.do_request('/apiserver/get_signed_urls', {'fnames': fnames})

    def proc(self, data: bytes):
        return self.do_request('/apiserver/proc', {'base64': base64_encode(data)})

    def req(self, urls):
        return self.do_request('/apiserver/req', {'urls': listify(urls)})

    def check(self, req_uid):
        return self.do_request('/apiserver/check', {'req_uid': req_uid})
