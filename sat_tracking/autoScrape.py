##AutoScrape.py

import time
from datetime import datetime
import webScraping as webS
while True:
  print("Web Scraping Running")
  webS.parser("https://www.amsat.org/tle/current/nasabare.txt")
  timePosted = str(datetime.now())
  timeUTC = str(datetime.utcnow())
  print("Time of Crawl(24 Hour Time): " + timePosted)
  print("Time of Crawl(UTC Time): " + timeUTC)
  #delay for 1 day
  time.sleep(24*60*60)
