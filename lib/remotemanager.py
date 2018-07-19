"""
Copyright (c) 2018, Digi International, Inc.
Module released under MIT License.

Module for easy interface with Digi Remote Manager.
Using documentation from "https://www.digi.com/resources/documentation/digidocs/90001437-13/default.htm#reference/r_ws_v1_streams.htm%3FTocPath%3DWeb%2520services%2520reference%7Cv1%252Fstreams%7C_____0"
    - Documentation does require an account to access

Use with samples/cellular/remotemanager/rm_sample.py.
"""

import ubinascii
import urequests

class AuthorizationException(Exception):
    pass

STREAMS_URI = "https://remotemanager.digi.com/ws/v1/streams/"

class RemoteManagerConnection:

    def __init__(self, auth_scheme="Basic", **credentials):
        if not credentials:
            self.auth = None
        else:
            self.set_auth(auth_scheme, **credentials)

    def set_auth(self, auth_scheme="Basic", **credentials):
        if auth_scheme == "Basic":
            self.auth = "Basic " + ubinascii.b2a_base64(credentials['username'] + ":" + credentials['password']).decode().strip()
        elif auth_scheme == "Bearer":
            self.auth = "Bearer " + credentials['token']
        else:
            raise AuthorizationException("Unsupported authorization scheme: " + auth_scheme)

    @staticmethod
    def check_response_code(response):
        if response.status_code not in (200, 201, 204):
            raise ConnectionError("Bad HTTP response status code: " + str(response.status_code))
        else:
            return response

    def set_headers(self, headers):
        if not self.auth:
            raise AuthorizationException("No authorization credentials provided")
        headers = dict() if headers is None else headers
        headers['Authorization'] = self.auth
        return headers

    def get_datastreams(self, headers=None):
        headers = self.set_headers(headers)
        response = urequests.get(STREAMS_URI + "inventory.json", headers=headers)
        self.check_response_code(response)
        return [stream['id'] for stream in response.json()['list']]

    def get_datastream_info(self, stream_id, headers=None):
        headers = self.set_headers(headers)
        response = urequests.get(STREAMS_URI + "inventory/" + stream_id + ".json", headers=headers)
        return self.check_response_code(response)

    def update_datastream(self, stream_id, json, headers=None):
        headers = self.set_headers(headers)
        response = urequests.put(STREAMS_URI + "inventory/" + stream_id, headers=headers, json=json)
        return self.check_response_code(response)

    def create_datastream(self, json, headers=None):
        headers = self.set_headers(headers)
        response = urequests.post(STREAMS_URI + "inventory/", headers=headers, json=json)
        return self.check_response_code(response)

    def delete_datastream(self, stream_id, headers=None):
        headers = self.set_headers(headers)
        response = urequests.delete(STREAMS_URI + "inventory/" + stream_id, headers=headers)
        return self.check_response_code(response)

    def add_datapoint(self, stream_id, value, headers=None):
        headers = self.set_headers(headers)
        response = urequests.post(STREAMS_URI + "history/", headers=headers, json={"stream_id": stream_id, "value": value})
        return self.check_response_code(response)

    def delete_datapoint(self, stream_id, start_time=None, end_time=None, headers=None):
        headers = self.set_headers(headers)
        response = urequests.delete(STREAMS_URI + "history/" + stream_id, params={"start_time": start_time, "end_time": end_time}, headers=headers)
        return self.check_response_code(response)
