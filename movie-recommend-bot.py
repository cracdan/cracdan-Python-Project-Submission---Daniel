from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def ScrapeImdbMovies():
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
    result = requests.get(url, headers=headers)

    soup = BeautifulSoup(result.content, 'html.parser')
    movieData = soup.find('script', id='__NEXT_DATA__')

    movieDict = {}

    if movieData:
        jsonData = json.loads(movieData.string)
        movies = jsonData['props']['pageProps']['pageData']['chartTitles']['edges']
        for movie in movies:
            title = movie['node']['titleText']['text']
            genres=[]

            for genre in list(movie['node']['titleGenres']['genres']):
                genres.append(genre['genre']['text'])
            movieDict[title]=genres
    else:
        print("ERROR")
    return movieDict

movieDict = ScrapeImdbMovies()

def WriteToCsv(movieDict):
    (pd.DataFrame.from_dict(data=movieDict, orient='index')
   .to_csv('movie_recommend.csv', header=False))

WriteToCsv(movieDict)


def ReadFromCsv():
    df = pd.read_csv("movie_recommend.csv")
    df.fillna('', inplace=True)
    extractedDict = df.set_index(df.columns[0]).T.to_dict(orient='list')
    return extractedDict

dictionary = ReadFromCsv()

def ReadGenreAndDisplayRecomendation(dictionary):
    search_term = input("Enter a search term: ").strip().lower()

# Find matching keys
    matching_keys = [key for key, values in dictionary.items() if search_term in map(str.lower, values)]

# Display results
    if matching_keys:
        print("Matching keys:","\n".join(matching_keys))
    else:
        print("No matches found.")

ReadGenreAndDisplayRecomendation(dictionary)