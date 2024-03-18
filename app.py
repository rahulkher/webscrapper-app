import scrappers.scrappers as scrappers
from scrappers.scrappers import ScrapeTwitter
import datetime
import os
from  dotenv import load_dotenv

load_dotenv()

# Use environment variables for credentials
username = os.getenv("TWITTER_USERNAME")
password = os.getenv("TWITTER_PASSWORD")

# Script to Scrape twitter data
query = "India Developping"
twitter = ScrapeTwitter((username, password), query=query)
login = twitter.login()
print(login["status"])

if login["status"] == "success":
    data = twitter.searchTwitter()
    # Format the current datetime in a filename-friendly format
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{query}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as file:
        # Assuming `data` is a JSON string; if `data` is a dictionary, use json.dump(data, file)
        file.write(data)
else:
    print(login["status"])
