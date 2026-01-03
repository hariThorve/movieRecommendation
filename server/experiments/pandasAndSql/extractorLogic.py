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



# movie name, ratings and vote count
def name_ratings_votecount(headers):
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
            movies_details.append({
                "name" : movie_name,
                "movie_ratings": ratings,
                "movie_genre" : [],
                "vote_counts" : vote_counts
            })
            
        except:
            movies_details.append(None)
    return movies_details 

# def find_genres(headers):
genre = []
for i in range(1, 11):
    try:

        response = requests.get("https://www.imdb.com/title/tt16431404/?ref_=sr_t_" + str(i), headers=headers)
        print(response)
        response.raise_for_status() # Check for bad status codes
        html_content = response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        exit()

    soup = BeautifulSoup(html_content, "html_parser")
    div = soup.find("div", class_="ipc-chip-list__scroller")
    hyperlink = div.find_all("a", class_="ipc-chip ipc-chip--on-baseAlt")
    print(hyperlink)
    genreList = [text for text in hyperlink.find_all("span", class_="ipc-chip__text").text]
    print(genreList)
    genre.append(genreList)
    
    # return genre

print(genre)
        









