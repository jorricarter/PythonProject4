# Meme Finder
Meme Finder is Flask powered WebApp meme search engine.
  - Access GIPHY, IMGUR, REDDIT API to find dank memes
  - Saves your favorite memes into MemeBox

# Installation
In terminal/command prompt, root directoty of the project.

### Setup virtual environment
Mac

    virtualenv -p python3 venv
    source venv/bin/activate

PC

    virtualenv venv
    venv/bin/activate

### Install required modules
Install requirments

    pip install -r requirements.txt

Install secrets.py module into the root folder

    file will be included during submission

Run app

    python webapp.py

App should be at 127.0.0.1:5000
For testing

    python -m unittest backEndTest.py

# Features

### Search
- Option to turn on off "meme only" for searching. On by default

### Meme
- I like this meme! button will save that meme to MemeBox

### MemeBox
- displays saved memes
- Confirms before deleting meme

### ETC
- something something

# Program File Structure/Desciprtion

    |- cache : meme search data cache file location
        |- cache.pickle : default cache file
    |- logs : log file location
        |- log.conf : logging configuration setting file
        |- memelog.log : default logging file
    |- memebox : bookmark data folder
        |- memebox.pickle : default bookmark data file
    |- static
        |- css
            |- style.css : stylesheet for the app
    |- templates : WebApp templates folder
        |- about.html
        |- index.html
        |- layout.html
        |- meme.html
        |- memebox.html
    |- backEndTest.py : unittest module for testing back ends
    |- memeCache.py : responsible for handling cache/MemeBox file I/O as well as cache verification/expired cache deletion
    |- memeFinder.py : master API module. Also handles cache/meme data for display
    |- memeFinderGiphy.py : GIPHY API module. API requests and create Meme objects
    |- memeFinderImgur.py : IMGUR API module. API requests and create Meme objects. Uses imgurpython for API calls
    |- memeFinderReddit.py : REDDIT API module. API requests and create Meme objects. Uses praw for API calls
    |- memeLogging.py : logging setup module
    |- requirements.txt : required module lists
    |- webapp.py : main program

# Extra
blah blah blah
