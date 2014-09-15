Hello OAuth World for GSpread
=============================


Currently, GSpread's documentation for its authorize() method does little more than tell you to read Google's manuals.  If you have small experience with OAuth, this can be a big problem, as in  -- many days down the drain.

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
  1. [Get Developer Credentials](#Get Developer Credentials)
  1. [Authenticate and self-authorize GMail SMTP use.](#Authenticate and self-authorize GMail SMTP use.)
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
<a name="Get Developer Credentials"/>
### Get Developer Credentials

The included utility [loadGoogleJSON.py](https://github.com/martinhbramwell/gspread_HelloOAuthWorld/blob/master/loadGoogleJSON.py) reads Google's OAuth credentials out of a JSON file that you have to download from [Google's Developer API console](https://console.developers.google.com/).

Follow these steps for [Obtaining Authentication Credentials from Google's new style API Console](https://github.com/martinhbramwell/gspread_HelloOAuthWorld/wiki/Obtaining-Authentication-Credentials-from-Google's-new-style-API-Console).


[Top](#Steps)

  
- - - - - - - - - - - - -
<a name="Authenticate and self-authorize GMail SMTP use."/>
### Authenticate and self-authorize GMail SMTP use.

Run the program [authorize_SMTP.py](https://github.com/martinhbramwell/gspread_HelloOAuthWorld/blob/master/authorize_SMTP.py)
    
    ./authorize_SMTP.py 
    
Since this is the first time you run it will ask for all details.  It remembers them, so that you have less to do on subsequent operations.

    No valid token pair found in working_parameters.py. Will run the wizard.
    Enter the GMail address you want to authorize : *<enter a GMail address here>*
    
Provide the GMail address for which you want to be authenticated as the official user for SMTP mail transfer, and you will be prompted as follows :

        To be able to request authorization from your users by email, you need to authorize this program to use Google's email resender in your name.
        Visit this url and follow the directions:

      https://accounts.google.com/o/oauth2/auth?client_id=181927152960-1525sfbj8lr7kh83q8q24f6rkijupfgk.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&scope=https%3A%2F%2Fmail.google.com%2F


        * * * Enter verification code:  <put the resulting code here>

Copy that url into a browser, follow the steps, then get the verification code and paste it into the field of the prompt "Enter verification code:" 

[http://imgur.com/delete/tJ2iaEVdSEmTxzS](http://i.imgur.com/cOaktkZ.png)
[http://imgur.com/delete/XUaxsXgqrqnfIar](http://i.imgur.com/ZaSKGlS.png)


[Top](#Steps)

asdfasdf
