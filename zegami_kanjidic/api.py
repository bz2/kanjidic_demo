# Copyright 2017 Zegami Ltd

"""API client for talking to Zegami cloud version."""

from __future__ import absolute_import

from . import (
    http,
)


# Some mimetypes for file upload
PNG_TYPE = "image/png"
TSV_TYPE = "text/tab-separated-values"


class Client(object):
    """HTTP client for interacting with the Zegami api."""

    def __init__(self, api_url, project, token):
        self.api_url = api_url
        self.project = project
        self.token = token
        auth = http.TokenEndpointAuth(api_url, token)
        self.session = http.make_session(auth)

    def create_collection(self, name, description=None):
        url = "{}v0/project/{}/collections/".format(self.api_url, self.project)
        info = {"name": name}
        if description is not None:
            info["description"] = description
        response_json = http.post_json(self.session, url, info)
        return response_json['collection']

    def update_collection(self, coll_id, info):
        url = "{}v0/project/{}/collections/{}".format(
            self.api_url, self.project, coll_id)
        response_json = http.put_json(self.session, url, info)
        return response_json['collection']

    def create_imageset(self, name, source=None):
        url = "{}v0/project/{}/imagesets/".format(self.api_url, self.project)
        info = {"name": name}
        if source is not None:
            info["source"] = source
        response_json = http.post_json(self.session, url, info)
        return response_json['imageset']

    def create_join(self, name, imageset_id, dataset_id):
        url = "{}v0/project/{}/datasets/".format(
            self.api_url, self.project)
        info = {
            "name": name,
            "source": {
                "imageset_id": imageset_id,
                "dataset_id": dataset_id,
                "imageset_name_join_to_dataset": {"dataset_column": "id"},
            }
        }
        response_json = http.post_json(self.session, url, info)
        return response_json["dataset"]

    def upload_data(self, dataset_id, path):
        url = "{}v0/project/{}/datasets/{}/file".format(
            self.api_url, self.project, dataset_id)
        response_json = http.post_file(self.session, url, path, TSV_TYPE)
        return response_json

    def upload_png(self, imageset_id, path):
        url = "{}v0/project/{}/imagesets/{}/images".format(
            self.api_url, self.project, imageset_id)
        response_json = http.post_file(self.session, url, path, PNG_TYPE)
        return response_json
