#!/usr/bin/env python
#
# Copyright 2007-2013 The Python-Twitter Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# credits given to developers on Python-Twitter
#
# https://github.com/bear/python-twitter
#
# The script has been modified to use Selenium to automate the process of getting
# twitter pincode. geckodriver needs to be installed

from __future__ import print_function

from requests_oauthlib import OAuth1Session
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'

#
# fetches OAUTH access_token and secret from  twitter api
# autoamted with selenium
#
def get_access_token(consumer_key, consumer_secret, user, passw):
    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri='oob')

    browser = webdriver.Firefox()

    print('\nRequesting temp token from Twitter...\n')

    try:
        resp = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)

    url = oauth_client.authorization_url(AUTHORIZATION_URL)

    print (url)

    browser.get(url)

    username = browser.find_element_by_id('username_or_email')
    username.send_keys(user)
    password = browser.find_element_by_id('password')
    password.send_keys(passw)

    allow_button = browser.find_element_by_id('allow')
    allow_button.click()

    # wait until pin pops up
    try:
        element = WebDriverWait(browser, 2).until(
                lambda driver : browser.find_element_by_tag_name("code")
        )
    finally:
        print ('yowp')

    pincode = element.text
    browser.quit()

    # access_token
    print('\nGenerating and signing request for an access token...\n')

    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret,
                                 resource_owner_key=resp.get('oauth_token'),
                                 resource_owner_secret=resp.get('oauth_token_secret'),
                                 verifier=pincode)
    try:
        resp = oauth_client.fetch_access_token(ACCESS_TOKEN_URL)
    except ValueError as e:
        print ("Invalid response from Twitter requesting temp token")
        pass

    print('''Your tokens/keys are as follows:
        consumer_key         = {ck}
        consumer_secret      = {cs}
        access_token_key     = {atk}
        access_token_secret  = {ats}'''.format(
            ck=consumer_key,
            cs=consumer_secret,
            atk=resp.get('oauth_token'),
            ats=resp.get('oauth_token_secret')))

    return  (resp.get('oauth_token'), resp.get('oauth_token_secret'))
