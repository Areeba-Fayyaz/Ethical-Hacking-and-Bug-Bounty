from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
#spider

# A set to keep track of visited URLs to avoid revisiting the same page
visited_urls = set()

# Function to spider through URLs and search for a specific keyword
def web_crawler(url, keyword):
    try:
        # Sending a request to the provided URL
        response = requests.get(url)
    except:
        # Handling exceptions in case the request fails
        print(f"Request failed {url}")
        return

    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Finding all 'a' tags to extract href attributes (links)
        a_tag = soup.find_all('a')
        urls = []  # List to store the found URLs

        # Looping through all 'a' tags
        for tag in a_tag:
            href = tag.get("href")
            # Ensuring href is not None and not empty
            if href is not None and href != "":
                # Appending the valid hrefs to urls list
                urls.append(href)

        # Iterating over each found URL
        for urls2 in urls:
            # Checking if the URL has already been visited
            if urls2 not in visited_urls:
                # Adding the new URL to the set of visited URLs
                visited_urls.add(urls2)
                
                # Constructing the absolute URL (in case of relative URLs)
                url_join = urljoin(url, urls2)
                # Checking if the keyword is in the URL
                if keyword in url_join:
                    print(url_join)
                    # Recursively calling spider_urls function
                    web_crawler(url_join, keyword)
            else:
                # Skipping the URL if it has already been visited
                pass

# Taking user input for the URL and keyword
url = input("Enter the URL you want to scrap: ")
keyword = input("Enter the keyword to search for in the URL provided: ")
# Initiating the spider process with the user-provided URL and keyword
web_crawler(url, keyword)


# https://www.yahoo.com
