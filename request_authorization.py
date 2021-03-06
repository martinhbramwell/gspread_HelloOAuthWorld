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
       Use this helper module to obtain permission from you users to access
       their Google Sheets.

'''

import os
import sys
import json
import argparse
import logging
import loadGoogleJSON

import urllib, urllib2, smtplib, time

from progressbar import Bar, Timer, ProgressBar, ReverseBar

parameters_file = 'working_parameters.py'

SCOPE = 'https://spreadsheets.google.com/feeds/'
class NameSpace(object):
  def __init__(self, adict):
    self.__dict__.update(adict)

credentials = None

try:

    from working_parameters import google_project_client_smtp_access_token
    from working_parameters import google_project_client_smtp_refresh_token
    from working_parameters import google_project_client_email
    
    assert len(google_project_client_smtp_refresh_token) == 45
    gpcsat_len = len(google_project_client_smtp_access_token)
    assert gpcsat_len > 50 and gpcsat_len < 80

    credentials = NameSpace(
      {
          "smtp_access_token" : google_project_client_smtp_access_token
        , "verification_url" : ""
        , "end_user_email" : ""
        , "client_email" : google_project_client_email
        , "user_code" : ""
        , "expiry" : ""
        , "device_code" : ""
        , "subject" : ""
        , "text" : ""
        , "x" : ""
      }
    )

except :

    sys.exit('No valid token pair found in {}. Please execute {}.'.format(parameters_file, 'authorize_SMTP.py'))
#    print 'Lengths : Access Token = {}, Refresh Token = {}.'.format(gpcsat_len, gpcsrt_len)


try :

    from oauth2 import GenerateOAuth2String
    from oauth2 import RefreshToken
    '''
    from oauth2 import GeneratePermissionUrl
    from oauth2 import AuthorizeTokens
    '''
    
except ImportError :

    # Get Google oauth2 helper file
    webFile = urllib.urlopen('http://google-mail-oauth2-tools.googlecode.com/svn/trunk/python/oauth2.py')
    localFile = open('oauth2.py', 'w')
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()
    
    from oauth2 import GenerateOAuth2String
    from oauth2 import RefreshToken
    '''
    from oauth2 import GeneratePermissionUrl
    from oauth2 import AuthorizeTokens
    '''


def third_person_auth(google_creds_, end_user_email_):

    logger.debug('Got Google credentialss : {}'.format(google_creds_.installed.client_secret))

#    google_project_client_smtp_access_token = smtp_credentials['access_token']
#    google_project_client_smtp_refresh_token = smtp_credentials['refresh_token']

    data = {}
    data['client_id'] = google_creds_.installed.client_id # 	the client_id obtained from the APIs Console 	Indicates the client that is making the request. The value passed in this parameter must exactly match the value shown in the APIs Console.
    data['scope'] = SCOPE  # Indicates the Google API access your application is requesting. The values passed in this parameter inform the consent page shown to the user. There is an inverse relationship between the number of permissions requested and the likelihood of obtaining user consent.
    
    url = 'https://accounts.google.com/o/oauth2/device/code'
    parms = urllib.urlencode(data)

    request = urllib2.Request (url, parms)

    theJSON = json.loads(urllib2.urlopen(request).read())
    logger.debug('Request : {}'.format(theJSON))
    

    credentials.verification_url = theJSON['verification_url']
    credentials.user_code = theJSON['user_code']
    credentials.expiry = int(theJSON['expires_in'])
    credentials.device_code = theJSON['device_code']
    
    credentials.subject = 'Requesting permission for remote access to your Google Spreadheets.'
    credentials.text = 'To give {} access to your spreadsheets, please copy this code [ {} ]'.format(credentials.client_email, credentials.user_code)
    credentials.text += ' to your clipboard, turn to {} and enter it in the'.format(credentials.verification_url)
    credentials.text += ' field provided. You have {} minutes to do so.'.format(credentials.expiry / 60)

    logger.debug('Verification_url : {}'.format(credentials.verification_url))
    logger.debug('End User Email : {}'.format(end_user_email_))
    logger.debug('Client Email : {}'.format(google_project_client_email))
    logger.debug('User Code : {}'.format(credentials.user_code))
    logger.debug('Expiry : {}'.format(credentials.expiry))
    logger.debug('Device Code : {}'.format(credentials.device_code))
    logger.debug('Subject : {}'.format(credentials.subject))
    logger.debug('Text : {}'.format(credentials.text))
    sending = True
    while sending :
        try :
        
            request_approval(credentials, end_user_email_)
            sending = False
            
        except smtplib.SMTPSenderRefused as sr :

            if sr[0] == 530 :
                if 'Authentication Required' in sr[1] :
                    print "  *    *   Do we get an 'invalid grant' error now ?   *    *    * "
                    sys.exit("We got an 'invalid grant' error. Authentication Required.")
                    
                print 'Refresh required: %s ' % google_project_client_smtp_refresh_token
                print 'Client ID: %s, Secret: %s ' % (google_creds_.installed.client_id, google_creds_.installed.client_secret)

                rslt = RefreshToken(
                      google_creds_.installed.client_id
                    , google_creds_.installed.client_secret
                    , google_project_client_smtp_refresh_token
                )
                print 'Result = {}'.format(rslt)
                if 'error' in rslt :
                    raise Exception("Cannot refresh invalid SMTP token. '%s' " % rslt['error'])
                    
                google_project_client_smtp_access_token = rslt['access_token']
                print 'New SMTP token : %s' % google_project_client_smtp_access_token
    
    return getAsForDevices(credentials, google_creds_, end_user_email_)


def getAsForDevices(credentials, google_creds_, end_user_email_) :
    m = 'ForDevices'

    subject = '%s wants permission to access your Google Spreadheets with "gspread".' % google_project_client_email
    
    print "\n\n* * * * *  You have to verify that you DO allow this software to open your Google document space."
    print     '* * * * *  Please check your email at %s.' % end_user_email_
    print     '* * * * *  The message, ["%s"]. contains further instructions for you.' % subject

    data = {}

    data['client_id'] = google_creds_.installed.client_id
    data['client_secret'] = google_creds_.installed.client_secret
    data['code'] = credentials.device_code
    data['grant_type'] = 'http://oauth.net/grant_type/device/1.0'
    
    url = 'https://accounts.google.com/o/oauth2/token'
    
    parms = urllib.urlencode(data)

    request = urllib2.Request (url, parms)

    delay = 30
    triesLimit = credentials.expiry
    print 'Trying to get tokens.'
    
    widgets = [Bar('>'), ' ', Timer(), ' ', ReverseBar('<')]
    with ProgressBar(widgets=widgets, maxval=triesLimit) as progress:
        for i in range(1, triesLimit, delay):

            theJSON = json.loads(urllib2.urlopen(request).read())

            if 'access_token' in theJSON :
                progress.finish()

#                print ' * * * Authorized ! * * * '
                credentials.oauth_access_token = theJSON['access_token']
                credentials.oauth_refresh_token = theJSON['refresh_token']

                return credentials
                
            elif 'error' in theJSON :
                time.sleep(delay)
                progress.update(i)
            else :
                progress.finish()
                print ' * * *  Uh oh ! * * * %s ' % theJSON

    print "Too late.  You'll have to repeat it all."
    exit(-1)    

def request_approval(credentials, end_user_email_) :

    # print "Temporary token using %s and %s ."   %  (google_project_client_email, store[theCurrentOAuthClient].smtp_access_token)
    auth_string = GenerateOAuth2String(google_project_client_email, credentials.smtp_access_token)
            
    message = 'From: <%s>\nTo: <%s>\nSubject: %s\n\n%s' % (
           google_project_client_email, end_user_email_, credentials.subject, credentials.text)
           

    logger.debug('\n\nEmail message\n{}'.format(message))
    logger.debug('\n\nAuth String : {}'.format(auth_string))
#    sys.exit('Quitting out of third_person_auth(google_creds_)')

    smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_conn.set_debuglevel(False)
    smtp_conn.ehlo('test')
    smtp_conn.starttls()
    
    smtp_conn.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    print 'Sending permission request . . . '
    smtp_conn.sendmail(google_project_client_email, end_user_email_, message)
    print ' . . permission request sent!'
    
    smtp_conn.close()


def prepare_result(credentials, google_creds_):

    creds_oa = open('creds_oa.py', 'w')
    creds_oa.write("\nrefresh_token = '{}'".format(credentials.oauth_refresh_token))
    creds_oa.write("\nclient_secret = '{}'".format(google_creds_.installed.client_secret))
    creds_oa.write("\nclient_id = '{}'".format(google_creds_.installed.client_id))
    creds_oa.write("\n#")
    creds_oa.write("\nkey_ring = {}")
    creds_oa.write("\nkey_ring['grant_type'] = 'refresh_token'")
    creds_oa.write("\nkey_ring['refresh_token'] = refresh_token")
    creds_oa.write("\nkey_ring['client_secret'] = client_secret")
    creds_oa.write("\nkey_ring['client_id'] = client_id")
    creds_oa.write("\n#")
    creds_oa.write("\naccess_token = '{}'".format(credentials.oauth_access_token))
    creds_oa.write("\n#\n#")
    creds_oa.write("\ncredentials = {")
    creds_oa.write("\n      'cred_type': 'oauth'")
    creds_oa.write("\n    , 'key_ring': key_ring")
    creds_oa.write("\n    , 'access_token': access_token")
    creds_oa.write("\n}")
    creds_oa.write("\n#")
    creds_oa.write("\nsmtp_access_token = '{}'".format(google_project_client_smtp_access_token))
    creds_oa.write("\nsmtp_refresh_token = '{}'".format(google_project_client_smtp_refresh_token))
    creds_oa.write("\n#")

    creds_oa.close()

    print 'Identify the Google spreadsheet you want to use; use the full URL ("http://" etc, etc) '
    spreadsheet_url  = raw_input('Paste the full URL here : ')
    #
    testScript = open('gspread_HelloOAuthWorld.py', 'w')
    testScript.write("#!/usr/bin/env python")
    testScript.write("\n# -*- coding: utf-8 -*-")
    testScript.write("\nimport gspread")
    testScript.write("\nfrom GSpreadCredentials import GSpreadCredentials")
    testScript.write("\n#")
    testScript.write("\nfrom creds_oa import key_ring")
    testScript.write("\n#")
    testScript.write("\ncr = GSpreadCredentials (None, key_ring)")
    testScript.write("\ngc = gspread.authorize(cr)")
    testScript.write("\n#")
    testScript.write("\nwkbk = gc.open_by_url('{}')".format(spreadsheet_url))
    testScript.write("\ncnt = 1")
    testScript.write("\nprint 'Found sheets:'")
    testScript.write("\nfor sheet in wkbk.worksheets():")
    testScript.write("\n    print ' - Sheet #{}: Id = {}  Title = {}'.format(cnt, sheet.id, sheet.title)")
    testScript.write("\n    cnt += 1")
    testScript.write("\n#\n")
    testScript.close()
    os.chmod('gspread_HelloOAuthWorld.py', 0o770)
    #
    print "\n\n   A simple example file called gspread_HelloOAuthWorld.py was written to disk."
    print "   It lists the names of the sheets in the target spreadsheet."
    print "   Test it with:"
    print "      $  python gspread_HelloOAuthWorld.py  ## or possibly just  ./gspread_HelloOAuthWorld.py\n\n\n"

pth = os.path.realpath(__file__)
PROG = pth.split(os.sep)[pth.count(os.sep)]

desc = 'Get authorization from your remote user to access their OAuth product.'
desc += '  The values are added to the file {}.'.format(parameters_file)
desc += '  If file {} already has all the necessary parameters no'.format(parameters_file)
desc += ' action is taken.'

msg_c = "to drop and create new credentials"
msg_k = "The identity key of a Google Spreadsheets workbook."
msg_r = "Row in Tasks sheet at which to start processing."


def get():

    usage = "usage: {} [options] arg".format(PROG)
    parser = argparse.ArgumentParser(description=desc, prog=PROG)

    msg_j = 'A json file of Google OAuth credentials from '
    msg_j += 'https://console.developers.google.com/ » [APIs & auth] » '
    msg_j += '[Credentials] » [Client ID for native application]'
    parser.add_argument(
        '-j'
      , '--client_id_json'
      , help=msg_j
      , required=False
    )
    parser.add_argument(
        '-e'
      , '--end_user_email'
      , help='The full GMail address of the other user whose permission you require.[e.g. your.friend@gmail.com]'
      , default=None
      , required=True
    )

    return parser.parse_args()



    
def main():
    
    args = get()


    google_creds = loadGoogleJSON.getCreds(args.client_id_json)
    logger.debug('               Client secret : {}\n'.format(google_creds.installed.client_secret))
    open(parameters_file, 'a').close()
    confirmation = third_person_auth(google_creds, args.end_user_email)

    prepare_result(confirmation, google_creds)
 
    return

if __name__ == '__main__':

    logging.FileHandler('python.log', mode='a')
    logger = logging.getLogger(PROG)
    logger.setLevel('DEBUG')
#    logger.setLevel('WARNING')
    
    main()
    exit(0)

