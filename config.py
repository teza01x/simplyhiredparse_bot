from html_dicts import *

# The number of pages that will be parsed will be on one site
# it is recommended no more than 3-4
total_pages = 3


# Text in a column
# column "Statut (Post On Discord, Post On Telegram, To Post)"
status = "Awaiting verdict"

# keywords for which the bot will search
# (you can add new words separated by commas in brackets)
# keywords = ["freelance", "free-lance"]
keywords = ["freelance", "free-lance"]

# path to your google chrome.exe browser
# Below is the standard path for windows, usually it is the same for everyone if you did not choose another during installation.
# Just in case, it is recommended to double-check.
# You also need to change this path if you have a different Linux / MacOS operating system
chrome_path = ""

countries = ["simplyhired.fr"]



# It's BETTER NOT TO TOUCH anything BELOW
# countries = ["simplyhired.fr", "simplyhired.be", "simplyhired.ch", "simplyhired.de", "simplyhired.ca",
#            "simplyhired.com.au", "simplyhired.com", "simplyhired.nl", "za.simplyhired.com", "simplyhired.pt",
#            "simplyhired.es", "simplyhired.ie", "simplyhired.co.uk", "simplyhired.se"]
country_dicts = [one, two]
platform = "simplyhired"
excel_name = "job_offers.xlsx"