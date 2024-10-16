# IMPAwards Movie Poster Downloader

![Logo](Assets/Logo.png)

Python3 Webscraper script for downloading official movie posters in the highest resolution available, using [impawards](https://impawards.com) as database.

## Installation & Quick Usage

### Executable:
* Download the latest executable from ['releases'](https://github.com/FdelMazo/PosterDownloader/releases/latest)
* After that, just start the PosterDownloader.exe (Windows) or write `./PosterDownloader` in the terminal (Linux)
    * Executables are generated with [PyInstaller](http://www.pyinstaller.org/) by just writing `pyinstaller posterdownloader.py -F`

### Python script:
* Clone repo `git clone https://github.com/FdelMazo/PosterDownloader.git`
* Install the dependencies `python setup.py install`
* Execute `python PosterDownloader.py`
        
## Complete options (Only when run on terminal):

`python PosterDownloader.py ["The Dark Knight 2008"] -flags` with the movie between brackets being optional and the -flags being:

* `-h, --help`            Show this help message and exit
* `-f FILE, --file FILE`  Bath download from a txt file
* `-y, --no-confirm`      No confirmation required from you
* `-a, --all`      Download every poster, instead of only the highest resolution available
* `--dry-run`             Only show what would be done, without modifying files
* `-l, --log`             Log everything to PosterDownlaoder.log
* `-v, --verbose`         Verbose/Debug logging
* `-q, --quiet`           Only log file modifications

### I have a problem! How can I contact you?

The easiest would be for you to describe your problem to me in the [issues](https://github.com/FdelMazo/posterdownloader/issues) section. To make it even easier you could replicate your error (search the same movies, pass the same txt file, etc etc) but this time logging it:
`Python posterdownloader.py --log`
* Comicbook Covers Downloader: https://github.com/FdelMazo/ComicbookCoversDownloader

* ---


 _____          _      _                                                 
|  ___|__  _ __| | __ | |__  _   _                                       
| |_ / _ \| '__| |/ / | '_ \| | | |                                      
|  _| (_) | |  |   <  | |_) | |_| |                                      
|_|  \___/|_|  |_|\_\ |_.__/ \__, |                                      
 __  __                      |___/_                                      
|  \/  | __ _ _ __ ___ ___    / ___|__ _ ___  __ _ _ __   _____   ____ _ 
| |\/| |/ _` | '__/ __/ _ \  | |   / _` / __|/ _` | '_ \ / _ \ \ / / _` |
| |  | | (_| | | | (_| (_) | | |__| (_| \__ \ (_| | | | | (_) \ V / (_| |
|_|  |_|\__,_|_|  \___\___/   \____\__,_|___/\__,_|_| |_|\___/ \_/ \__,_|



  FORK BY MarcoCasanova00:

  Now it's possible to choose from a range of dates and a range of movies from the result list.
* 
