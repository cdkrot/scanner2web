Scanner2web home
----------------

Scanner2web is simple web application to make your scanner available across network.

It is written in pure wsgi, and will run on any wsgi-capable server.

You just need to install it on linux or unix machine with scanner, and give other people
web address to use.

Requirements
------------

* python3, for running the scanner2web itself.
* scanimage (from sane), for interacting with scanner.
* convert (from imagemagick), for on-the-fly convertions to png.

Checking:
$ python3 --version
Should produce something like 'Python 3.4.3'

$ scanimage > image.pnm && file image.pnm
Should produce something like 'Netpbm PPM "rawbits" image data, size = ....'

$ scanimage | convert pnm:- png:image.png && file image.png
Should produce something like 'image.png: PNG image data, ...'

Installation
------------

* download all files in this repo
$ git clone <path-to-this-repo> # for example

* Run any wsgi server, with main.py as application.
If you are short on time, you can just run:

$ ./serve.py

It will host scanner2web on :8080 on all IP interfaces.

Urls
----

/           - for the main page itself
/script.js  - for the script file
/style.css  - for styles
/image.png  - returns the last scanned image.
/rescan     - triggers a rescan

No other URLS are available regardless of files in scanner2web directory.
So feel free to store any other files in it.

Files used
----------

serve.py    - simple wsgi server.
main.py     - scanner2web app
script.js   - javascript for browser
style.css   - styles for browser
index.html  - main page
rescan.html - returned to javascript-free browsers on '/rescan' request
image.png   - [temporary file] stores last scanned image
image.lock  - [temporary file] prevents data races.

No other files are used.
