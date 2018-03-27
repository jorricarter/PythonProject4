# Meme Finder
Meme Finder is Flask powered WebApp meme search engine.
  - Access GIPHY, IMGUR, REDDIT API to find dank memes
  - Save your favorite memes into MemeBox

# Installation
In terminal/command prompt, root directoty of the project.

### Setup virtual environment
Mac

    virtualenv -p python3 venv
    source venv/bin/activate

PC

    virtualenv venv
    venv/scripts/activate

### Install required modules
Install requirments

    pip install -r requirements.txt

Install secrets.py module into the root folder

    secrets.py file will be included during submission

Run app

    python webapp.py

App should be at 127.0.0.1:5000
For testing

    python -m unittest tests.back_end_test
    python -m unittest tests.front_end_test

# Features

### Search
- Option to turn on off "meme only" for searching. On by default

### Meme
- I like this meme! button will save that meme to MemeBox

### MemeBox
- displays saved memes
- Confirms before deleting meme

### ETC
- create/login as user to save & access MemeBox

# Program File Structure/Desciprtion

    |- db : db folder for cache and MemeBox 
        |- gif_finder_db.db : default db file
    |- logs : log file location
        |- log.conf : logging configuration setting file
        |- memelog.log : default logging file
    |- static
        |- css
            |- style.css : stylesheet for the app
    |- templates : WebApp templates folder
        |- about.html : basic information about Meme Finder
        |- index.html : main menu
        |- layout.html : main layout for the header/footer
        |- login_page.html : login page
        |- meme.html  : result page
        |- memebox.html : MemeBox/bookmark page
        |- signup.html : signup page
    |- tests : testing modules folder
        |- back_end_test.py  : unittest module for testing back ends
        |- front_end_test.py : selenium powered automated front end test module
    |- classes.py : contains Meme class definition
    |- db_sqlite.py : db module
    |- geckodriver.exe : firefox driver required for front end test. Handles cache/bookmark I/O
    |- meme_finder.py : master API module. Also handles cache/meme data for display
    |- meme_finder_giphy.py : GIPHY API module. API requests and create Meme objects
    |- meme_finder_imgur.py : IMGUR API module. API requests and create Meme objects. Uses imgurpython for API calls
    |- meme_finder_reddit.py : REDDIT API module. API requests and create Meme objects. Uses praw for API calls
    |- meme_logging.py : logging setup module
    |- requirements.txt : required module lists
    |- webapp.py : main program

