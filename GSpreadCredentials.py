#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''

   The full program is explained in the attached ReadMe.md

    Copyright (C) 2013 warehouseman.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Created on 2013-03-19

    @author: Martin H. Bramwell

    This module:
       This is a simple Credential object as so curtly required here : 
        - http://burnash.github.io/gspread/oauth2.html#custom-credentials-objects

'''

from json import loads
try:
    import httplib as client
    from urlparse import urlparse
    from urllib import urlencode
except ImportError:
    from http import client
    from urllib.parse import urlparse
    from urllib.parse import urlencode

GOOGLE_OAUTH_TOKEN_REFRESH_URL = "https://accounts.google.com/o/oauth2/token"

class GSpreadCredentials (object):

  def __init__ (self, access_token_=None, key_ring_=None):
#    print"## {} ##".format(access_token_)
    self.access_token = access_token_
    self.key_ring = key_ring_

  def refresh (self, http_):
    '''
    Performs a token refresh cycle as described here :
       https://developers.google.com/youtube/v3/guides/authentication#OAuth2_Refreshing_a_Token
    '''
#    print "Key ring has : {}".format(self.key_ring['refresh_token'])
    parms = urlencode(self.key_ring)
    req_hdrs = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = urlparse(GOOGLE_OAUTH_TOKEN_REFRESH_URL).netloc

    conn = client.HTTPSConnection(url)
    conn.request('POST', GOOGLE_OAUTH_TOKEN_REFRESH_URL, parms, headers=req_hdrs)
    response = conn.getresponse()

    self.access_token = loads(response.read().decode())['access_token']
    return

