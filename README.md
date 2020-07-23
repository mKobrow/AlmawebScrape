# AlmawebScrape
Scrapes out the results of tests and sends you an email as soon as there is a new one.

## Required Software
- Python3
- screen

## Required Python3 Libs
- requests
- bs4
- email  
They may be already installed, if not just install with `pip3`.

## Instructions
Rename the `config_blanko.py` to `config.py`and edit it.
Put the Files onto your Server and use `./startscript.sh start` to start the Service.
If its working you should recieve an email.
