# Copyright 2017 Zegami Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for making http requests."""

import requests


def download(session, url, filename):
    """Fetch url and write into filename."""
    with session.get(url, stream=True) as response:
        response.raise_for_status()
        _pump_to_file(response.raw, filename)


def _pump_to_file(source, filename, _chunk_size=(1 << 15)):
    with open(filename, "wb") as f:
        while True:
            data = source.read(_chunk_size)
            if not data:
                break
            f.write(data)


class TokenEndpointAuth(requests.auth.AuthBase):
    """Request auth that adds bearer token for specific endpoint only."""

    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token

    def __call__(self, request):
        if request.url.startswith(self.endpoint):
            request.headers["Authorization"] = "Bearer {}".format(self.token)
        return request


def make_session(auth=None):
    """Create a session object with optional auth handling."""
    session = requests.Session()
    session.auth = auth
    return session


def post_json(session, url, python_obj):
    """Send a json request and decode json response."""
    with session.post(url, json=python_obj) as response:
        response.raise_for_status()
        return response.json()


def post_file(session, url, name, filelike, mimetype):
    """Send a data file."""
    details = (name, filelike, mimetype)
    with session.post(url, files={'file': details}) as response:
        response.raise_for_status()
        return response.json()


def put_file(session, url, filelike, mimetype):
    """Put binary content and decode json respose."""
    headers = {'Content-Type': mimetype}
    with session.put(url, data=filelike, headers=headers) as response:
        response.raise_for_status()
        return response.json()


def put_json(session, url, python_obj):
    """Put json content and decode json response."""
    with session.put(url, json=python_obj) as response:
        response.raise_for_status()
        return response.json()
