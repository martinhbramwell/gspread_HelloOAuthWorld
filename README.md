Hello OAuth World for GSpread
=============================


Currently, GSpread's documentation for the authorize() method does little more than tell you to read Google's manuals.  If you have small experience with OAuth, this can be a big problem, as in  -- many days down the drain.

This example should get you going quickly, as long as you already have Python running in Ubuntu.  Everything else is explained step by step.

Note that that OAuth has several versions and numerous distinct sequences of operations for different purposes and circumstances.  One of the trickiest parts of learning OAuth is that different document authors use different terminology to refer to the same sequence or simply fail to clarify which sequence or version they're talking about.

This Hello World shows you how to perform these two different sequences :

  1. authenticate and authorize yourself to use your own GMail account as a mail transfer service for your Python programs.  It uses the OAuth sequence described in [Using OAuth 2.0 for Web Server Applications](http://goo.gl/CLzxPZ).
  2. get a third-party to authorize you to access their Google Sheets.  It uses the OAuth sequence described in [Using OAuth 2.0 for Devices](http://goo.gl/EGfc8e).

<a name="authorize_SMTP.py"/>
##### authorize_SMTP.py
The included program [authorize_SMTP.py](http://goo.gl/nBJ3bE) works in accordance with this sequence:

<p align="center">
  <img src="http://i.imgur.com/HAuXGjA.png" alt="http://imgur.com/delete/DAT65Rc0ipSc3BY"/>
</p>


It prepares and displays a URL that includes a request token, and then prompts you to enter an authorization code.  When you open the URL in a browser, you will need to log in to Google (if you haven't done so earlier) and consent to the indicated permissions.  You then copy the resulting code back into the command line of [authorize_SMTP.py](http://goo.gl/nBJ3bE).  It will write to disk a file called *"working_parameters.py"*.  Imported into any other Python program, that file will provide the access and refresh tokens for using GMail as an SMTP mail transfer service.


<a name="request_authorization.py"/>
##### request_authorization.py
The included program [request_authorization.py](http://goo.gl/MiqfQ4) works in accordance with this sequence :
<p align="center">
  <img src="http://i.imgur.com/zGuwWFZ.png" alt="http://imgur.com/delete/CurGk13H48bjiMf"/>
</p>

It connects to Google and obtains a URL and authorization code for accessing a thrid-party's Google Sheets, then prepares an email and sends it to that individual. The text of the email explains to them the purpose of the authorization code and provides a hyperlink to the authorization page.  They simply have to copy and paste the provided code into the field presented at that URL, and then consent to the indicated access permissions on Google Sheets.

Meanwhile, from the moment it sends the email, [request_authorization.py](http://goo.gl/MiqfQ4) sits in a slow loop waiting for 30 minutes, for your user to react.  If they do indeed authorize you, [request_authorization.py](http://goo.gl/MiqfQ4) will prompt you to enter the URL of one of their Google Sheets workbooks, then writes two files to disk: a new credentials file called *"creds_oa.py"*, and an executable Python script *"gspread_HelloOAuthWorld.py"*.  The latter uses the former and GSpread to get and display the name of the first sheet of your user's workbook. 



<a name="Steps"/>
Here are the steps :

  1. [Get the code](#Get the code)
  1. [Start up a Virtual Environment](#Start up a Virtual Environment)
  1. [Resolve Dependencies](#Resolve Dependencies)
  1. [Get Developer Credentials](#Get Developer Credentials)
  1. [Authenticate and self-authorize GMail SMTP use.](#Authenticate and self-authorize GMail SMTP use.)
  1. [Get permission on other user's spreadsheet.](#Get permission on other user's spreadsheet.)
  2. 
  3. 

- - - - - - - - - - - - -
<a name="Get the code"/>
### Get the code

    # Make a disposable directory
    mkdir -p ~/disposable
    #
    # Jump into it
    pushd ~/disposable
    #
    # Get the code
    wget https://github.com/martinhbramwell/gspread_HelloOAuthWorld/archive/master.zip
    #
    # unpack it
    unzip master.zip
    #
    # give it its real name
    mv gspread_HelloOAuthWorld-master gspread_HelloOAuthWorld
    #
    popd
    #
    

[Top](#Steps)

  
- - - - - - - - - - - - -
<a name="Start up a Virtual Environment"/>
### Start up a Virtual Environment

I don't want to be accused of wrecking anyone's system.  Python is integral to the workings of Ubuntu and altering it willy-nilly is a bad idea.  Virtual environments protect you from that.

First we check what the Python execution path looks like normally.  It contains directories like `/usr/local/...` and  `/usr/lib/...` etc.  That's what we do *not* want to mess up.

    python -c "import sys; print sys.path"

Now we can prepare for virtual environment management

    pushd ~/disposable/gspread_HelloOAuthWorld
    sudo ./prepare_virtualenv.sh

The scripts create new environment variables and aliases that will be available on next log in.  To get them now, run this . . .

    source ~/.bashrc

We create a shadow directory holding the secluded execution environment for our project.

    mkvirtualenv hiOAWorld

Notice that your execution prompt is now prefixed with `(hiOAWorld)`. Check if the execution path is now self-contained.  You should see numerous references to a directory `/home/yourself/.python_virtual_environments/hiOAWorld/`

    python -c "import sys; print sys.path"

Deactivate the created virtual project

    deactivate

Check it again.  The `(hiOAWorld)` prefix should be gone.

    python -c "import sys; print sys.path"

Reactivate the virtual project.

    workon hiOAWorld

Check it again.  The `(hiOAWorld)` prefix should be back again.

    python -c "import sys; print sys.path"

Go back to where you were before

    popd


[Top](#Steps)


- - - - - - - - - - - - -
<a name="Resolve Dependencies"/>
### Resolve Dependencies

The application has a few external dependencies.  Now is the time to go get them.

Make sure you are "in" the virtual enviroment:

     workon hiOAWorld
     
Now you can safely install the dependencies:

     pip install progressbar2 gspread httplib2

[Top](#Steps)


- - - - - - - - - - - - -
<a name="Get Developer Credentials"/>
### Get Developer Credentials

The included utility [loadGoogleJSON.py](https://github.com/martinhbramwell/gspread_HelloOAuthWorld/blob/master/loadGoogleJSON.py) reads Google's OAuth credentials out of a JSON file that you have to download from [Google's Developer API console](https://console.developers.google.com/).

Follow these steps for [Obtaining Authentication Credentials from Google's new style API Console](https://github.com/martinhbramwell/gspread_HelloOAuthWorld/wiki/Obtaining-Authentication-Credentials-from-Google's-new-style-API-Console).

You will need to save the file *"client_secret_xxx...xxx.apps.googleusercontent.com.json"* in the directory *"~/disposable/gspread_HelloOAuthWorld"*.


[Top](#Steps)
  
- - - - - - - - - - - - -
<a name="Authenticate and self-authorize GMail SMTP use"/>
### Authenticate and self-authorize GMail SMTP use.
  
Run the program [authorize_SMTP.py](https://github.com/martinhbramwell/gspread_HelloOAuthWorld/blob/master/authorize_SMTP.py)
    
    ./authorize_SMTP.py 
    
The first time you run it, it will ask for all details.  It remembers them so that you have less to do on subsequent operations.

    No valid token pair found in working_parameters.py. Will run the wizard.
    Enter the GMail address you want to authorize : *<enter a GMail address here>*
    
Provide the GMail address for which you want to be authenticated as the official user for SMTP mail transfer, and you will be prompted as follows :

        To be able to request authorization from your users by email, you need to authorize this program to use Google's email resender in your name.
        Visit this url and follow the directions:

      https://accounts.google.com/o/oauth2/auth?client_id=181927152960-1525sfbj8lr7kh83q8q24f6rkijupfgk.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&scope=https%3A%2F%2Fmail.google.com%2F


        * * * Enter verification code:  <put the resulting code here>

Copy that url into a browser, follow the steps, then get the verification code and paste it into the field of the prompt "Enter verification code:" 


#### "User login and consent" step . . . 
<p align="center">
  <img src="http://i.imgur.com/cOaktkZ.png" alt="http://imgur.com/delete/tJ2iaEVdSEmTxzS"/>
</p>

#### "Authorization code" response step . . . 
<p align="center">
  <img src="http://i.imgur.com/ZaSKGlS.png" alt="http://imgur.com/delete/XUaxsXgqrqnfIar"/>
</p>

Shortly after pasting the code and hitting [Enter] the following should appear :

      Success :
       - Access Token: = ya29.gQB-6n3zy3BzENT3w9Bs4F97s-i6TdoNd_3Gpk5PHtpfwZgmVlAofiGA
       - Refresh Token: 1/RevA7ZIJdKPaXVidCBRuyv93jv3FWRkSBs5l8qkv5wM
       - Access Token expires at : 2014-09-15 17:39
      Appending latest tokens to the bottom of the file "working_parameters.py". . . 
       . . done.

      No test mail sent.

Also, a new file is written to disk, available to the next step.  *"working_parameters.py"* contains : 

     # Appended automatically . . . 
     google_project_client_smtp_access_token = 'ya29.gQB-6n3zy3BzENT3w9Bs4F97s-i6TdoNd_3Gpk5PHtpfwZgmVlAofiGA'
     google_project_client_smtp_refresh_token = '1/RevA7ZIJdKPaXVidCBRuyv93jv3FWRkSBs5l8qkv5wM'
     google_project_client_smtp_expiry = '2014-09-15 17:39'
     google_project_client_email = 'doowa.diddee@gmail.com'
     #


[Top](#Steps)
  
- - - - - - - - - - - - -
<a name="Get permission on other user's spreadsheet."/>
### Get permission on other user's spreadsheet.

Now that we can send email through Google SMTP, we can request access to Google products of other users.

Run the following command, replacing *[some.other.user.name@gmail.com]* for the GMail address of a real user, of course :

     ./request_authorization.py  -e some.other.user.name@gmail.com
     
Text like the following will be displayed :

     Sending permission request . . . 
      . . permission request sent!


     * * * * *  You have to verify that you DO allow this software to open your Google document space.
     * * * * *  Please check your email at some.other.user.name@gmail.com.
     * * * * *  The message, [doowa.diddee@gmail.com wants permission to access your Google Spreadheets with "gspread".] contains further instructions for you.
     Trying to get tokens.
     |>>>>            | Elapsed Time: 0:06:33 |             <<<<<|
     
Your user will see an email like this :

<p align="center">
  <img src="http://i.imgur.com/mD9jQtb.png" alt="http://imgur.com/delete/NxuM5YDOkoSCuz5"/>
</p>

They will copy the indicated code and paste it into a screen like this :

<p align="center">
  <img src="http://i.imgur.com/prCopC0.png" alt="http://imgur.com/delete/A45XpQGOdGlCPse"/>
</p>

Your user will approve by clicking the blue button . . .

<p align="center">
  <img src="http://i.imgur.com/MMKrulr.png" alt="http://imgur.com/delete/WhPW9zaIZJleq9H"/>
</p>

. . . and see a confirmation screen like this :

<p align="center">
  <img src="http://i.imgur.com/b85wiew.png" alt="http://imgur.com/delete/PBcmu0ueLIFWHb7"/>
</p>


If your user takes longer than 30 minutes you'll have to try again.

If your user does approve the *"./request_authorization.py"* program will continue to the next step with a screen like this :

        Code fragment to use to configure the gspread 'nose' tests.  Paste into the file 'test.config' : 
        .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 

        auth_type: OAuth
        ;
        ; These three values are obligatory for OAuth access, not required for UID/pwd access
        client_secret: dZkFOCokPpIwE8WjWtsHJ4Dh
        client_id: 181927152960-1525sfbj8lr7kh83q8q24f6rkijupfgk.apps.googleusercontent.com
        refresh_token: 1/0ganAW-pDLac532zRHU6AjE8og99_mxHBmFGDu6I2QY

        ; This value is optional but will make the tests start sooner if the token is less than 60 minutes old.
        access_token: ya29.ggAIFzx08HBNfUcuNVK3Ws_82ktn-LLBSHVwHGimMPHU0c_N09OgHoDz

         .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 
        Identify the Google spreadsheet you want to use; use the full URL ("http://" etc, etc) 
        Paste the full URL here : <full Google Sheets URL here>
        
The penultimate step is to enter the URL of one your user's spreadsheets at the prompt, "Paste the full URL here : ".  A quick test file will have been generated :

        A simple example file called gspread_HelloOAuthWorld.py was written to disk.
        It lists the names of the sheets in the target spreadsheet.
        Test it with:
           $  python gspread_HelloOAuthWorld.py  ## or possibly just  ./gspread_HelloOAuthWorld.py

*"./gspread_HelloOAuthWorld.py"* is an extremely simple sample that you can use as starting point for more complex projects.
[Top](#Steps)
  
- - - - - - - - - - - - -
<a name="Get permission on other user's spreadsheet."/>
### Run .

[Top](#Steps)



