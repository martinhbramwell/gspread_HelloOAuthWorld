Hello OAuth World for GSpread
=============================


The documentation for GSpread's authorize() method does little more than tell you to read Google's manuals.  For those with little experience with OAuth, unecessarily this may be a big problem, as in  -- many days down the drain.

If you have Python in Ubuntu this should get you going.

<a name="Steps"/>
Here are the steps :

  1. [Get the code](#Get the code)
  1. [Set up a Virtual Environment](#Set up a Virtual Environment)
  1. [Get Developer Credentials](#Get Developer Credentials)
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
    git clone git@github.com:martinhbramwell/gspread_HelloOAuthWorld.git
    #
    popd
    #
    

[Top](#Steps)

  
- - - - - - - - - - - - -
<a name="Set up a Virtual Environment"/>
### Set up a Virtual Environment

I don't want do be accused of wrecking anone's system.  Python is integral to the workings of Ubuntu and altering it willy-nilly is a bad idea.  Virtual environments protect you from that.

First we prepare for virtual environment management

    sudo ./prepare_virtualenv.py

We need a directory for our virtual project

    pushd ~/disposable/gspread_HelloOAuthWorld
    mkdir -p ../venv

We advise the virtual environment manager that it is there

    mkvirtualenv ../venv
    popd

Check if the execution path is now fully self-contained

    python -c "import sys; print sys.path"

Deactivate the created virtual project

    deactivate

Reactivate the virtual project

    workon venv

Check it again

    python -c "import sys; print sys.path"


[Top](#Steps)

  
- - - - - - - - - - - - -
<a name="Get Developer Credentials"/>
### Get Developer Credentials

Resolve all dependencies

    pip install oauth2client

[Top](#Steps)

asdfasdf
