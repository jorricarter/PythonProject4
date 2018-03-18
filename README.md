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

Configure environment variables

    Set envar. Need to research for the best practice

Run app

    python webapp.py

App should be at 127.0.0.1:5000
For testing

    python -m tests.... something like this

# Features

### Search
- Option to turn on off "meme only" for searching. On by default

### Meme
- something something

### MemeBox
- displays blah
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
    |- tests : app testing module folder
        |- test_memeFinder.py
        |- test_memeFinderGiphy.py
        |- test_memeFinderImgur.py
        |- test_memeFinderReddit.py
        |- test_memeLogging.py
        |- test_webapp.py
    |- memeCache.py
    |- memeFinder.py
    |- memeFinderGiphy.py
    |- memeFinderImgur.py
    |- memeFinderReddit.py
    |- memeLogging.py
    |- requirements.txt : required module lists
    |- webapp.py : main program

# Extra
blah blah blah