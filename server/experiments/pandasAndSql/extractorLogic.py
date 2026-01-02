# Flow

# Problem statement : fetch top 10 movies and add it to database in following format

"""
{
    "name": "movieName",
    "genre": "",
    "rating": "",
    "no_of_votes": "",

}
"""
# 1. fetch data through websracpping IMDB
# 2. add them to sql Database

import requests 
from bs4 import BeautifulSoup
from schema import sessionDependency, create_table

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

try:
    response = requests.get("https://www.imdb.com/search/title/?moviemeter=,10", headers=headers)
    response.raise_for_status() # Check for bad status codes
    html_content = response.content
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()



soup = BeautifulSoup(html_content, "html.parser")
ul = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-d24d5d37-0 hDHQeM detailed-list-view ipc-metadata-list--base")

movies_details = []



for li in ul.find_all("li", class_="ipc-metadata-list-summary-item"):
    div = li.find("div", class_="sc-b4f120f6-0 bQhtuJ")
    movie_name = div.find("h3").get_text()
    try:
        ratings = div.find("span", class_="ipc-rating-star--rating").get_text()
        vote_counts = div.find("span", class_="ipc-rating-star--voteCount").get_text()
        
    except:
        movies_details.append(None)
    # ratings = div.find("span", class_="ipc-rating-star--rating").get_text()

    
print(movies_details)