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

    Created on 2014-09-15

    @author: Martin H. Bramwell

    This module:
       This is a helper utility for reading the JSON file that you download 
       from --- https://console.developers.google.com/ in the sub-section :
         - your API Project
           - APIs & auth 
             - Credentials 
               - Client ID for native application
                  - [Download JSON]

    You will be able to access you data as a "dot formatted" name space.
    
    json_data = getCreds("client_sec...xxx...oogleusercontent.com.json")
    client_id = json_data.installed.client_id
    client_secret = json_data.installed.client_secret
    
'''

import os
import jsonio
import logging

logging.basicConfig(filename='python.log',level=logging.WARNING)

def getCreds(filename) :

  json_files = []
  cnt = 0
  if filename :
    json_files.append(filename)
    cnt = 1
  else :
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    cnt = 0;
    for f in files:
        if f.endswith('.json'):
            cnt += 1;
            json_files.append(f)
      
  theFile = None
  
  if cnt < 1:
      print '\n\nCould not find exactly one (1) expected json file (named like "client_secret_*.json" for example).'
      print 'You get such a file from : https://console.developers.google.com/ in the sub-section :'
      print '   - your API Project'
      print '     - APIs & auth '
      print '       - Credentials '
      print '         - Client ID for native application'
      print '            - [Download JSON]'
      print ' '
      return None
              
  else:
      theFile = json_files[0]
      if cnt > 1:
          print '\n\nPlease type the number of the json file that contains the credentials you want to try.'
          cnt = 0
          for jf in json_files:
              cnt += 1;
              print '{}) -- {}'.format(cnt, jf)
          theFile = json_files[int(raw_input('Which? ')) - 1 ]
      
      json_data = jsonio.getObj( theFile )
      
      logging.debug('\n The file "{}" contains :\n'.format(theFile))
      logging.debug('               Client id : {}'.format(json_data.installed.client_id))
      logging.debug('               Client secret : {}\n'.format(json_data.installed.client_secret))

  return json_data
  
