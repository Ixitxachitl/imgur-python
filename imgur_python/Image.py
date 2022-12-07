#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Image handler
"""

import requests
from .ImgurBase import ImgurBase


class Image(ImgurBase):
    "Class to handle images in the imgur account"

    def __init__(self, config, api_url):
        self.config = config
        self.api_url = api_url

    def get_header(self):
        if self.config.get('access_token'):
            headers = {
                'authorization': 'Bearer {0}'.format(self.config['access_token'])
            }
        else:
            headers = {
                'authorization': f'Authorization: Client-ID {self.config["client_id"]}'
            }
        return headers


    def images(self, page):
        "Get account images"
        url = '{0}/3/account/me/images/{1}'.format(
            self.api_url,
            page
        )
        request = requests.get(url, headers=self.get_header())
        response = self.response(request, url)
        # the total number of comments
        response['response']['total'] = self.count()
        return response

    def image(self, image_id):
        "Get information about an image"
        url = '{0}/3/image/{1}'.format(self.api_url, image_id)
        request = requests.get(url, headers=self.get_header())
        return self.response(request, url)

    def upload(self, payload, files=None):
        "Upload a new image or video"
        url = '{0}/3/upload'.format(self.api_url)
        if files is not None:
            request = requests.post(
                url,
                headers=self.get_header(),
                data=payload,
                files=files
            )
        else:
            request = requests.post(url, headers=self.get_header(), data=payload)
        return self.response(request, url)

    def update(self, image_id, payload):
        "Updates the title or description of an image"
        url = '{0}/3/image/{1}'.format(self.api_url, image_id)
        request = requests.post(url, headers=self.get_header(), data=payload)
        return self.response(request, url)

    def delete(self, image_id):
        "Deletes an image"
        url = '{0}/3/image/{1}'.format(self.api_url, image_id)
        request = requests.delete(url, headers=self.get_header())
        return self.response(request, url)

    def ids(self, page):
        "Returns an array of Image IDs that are associated with the account"
        url = '{0}/3/account/{1}/images/ids/{2}'.format(
            self.api_url,
            self.config['account_username'],
            page
        )
        request = requests.get(url, headers=self.get_header())
        response = self.response(request, url)
        # the total number of comments
        response['response']['total'] = self.count()
        return response

    def fav(self, image_id):
        "Favorite an image with the given ID"
        url = '{0}/3/image/{1}/favorite'.format(self.api_url, image_id)
        request = requests.post(url, headers=self.get_header())
        return self.response(request, url)

    def count(self):
        "Return the total number of albums associated with the account"
        url = '{0}/3/account/{1}/images/count'.format(
            self.api_url,
            self.config['account_username']
        )
        request = requests.get(url, headers=self.get_header())
        return self.data(request)
