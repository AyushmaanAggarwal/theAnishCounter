import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random
import urllib

def to_numeric(string, num_type='int'):
    '''
    Function to strip all non-numeric characters from string and return int or float
    INPUT - String to convert
          - num_type: either 'int' or 'float'
    OUTPUT - int or float type (returns original string if neither specified)
    '''
    if num_type == 'float':
        x = float( re.sub("[^0-9]", "", string ) )
    elif num_type == 'int':
        x = int( re.sub("[^0-9]", "", string ) )
    else:
        x = string
    return x

def imdb_scrape(imdb_id):
    '''
    Function which scrapes IMDb using IMDb ID 'tt0107290'. Second parameter is for 
    the movie poster (saved in /posters/ folder). Third parameter is to print result.
    
    This function is mean to be used in a loop. As such, the print outputs may lack
    meaning if used outside of the cells below.
    
    INPUT:  - ID of movie to scrape from IMDB e.g. "tt0076759"
            - boolean to save the movie poster or not (default True)
            - boolean to print result
           
    OUTPUT: Dictionary of various scrapped information.
    
             {'tconst':imdb_id, 'title':'',     'release_year':'',     'release_date':'',
              'MPAA':'',        'genre':[],     'runtime':'',          'poster_url':'',
              'plot_short':'',  'plot_long':'', 'imdb_rating':'',      'num_imdb_votes':'',
              'metacritic':'',  'num_user_reviews':'',                 'num_critic_reviews':''
             }
    '''
    # Target datapoints to scrape (with provided imdb_id)
    imdb_info_dict = {'tconst':imdb_id,'title':'',    'release_year':'',      'release_date':'',
                      'MPAA':'',       'genre':[],    'runtime':'',           'poster_url':'',
                      'plot_short':'', 'plot_long':'', 'imdb_rating':'',      'num_imdb_votes':'',
                      'metacritic':'', 'num_user_reviews':'',                 'num_critic_reviews':''
                     }
    imdb_info_dict['tconst'] = imdb_id
    
    imdb_base_url = 'https://www.imdb.com/title/'
    print(f'{imdb_id.ljust(10)} ', end='')

    API_KEY = 'b9a0563b-3513-4500-83f0-966779396518'

    def get_scrapeops_url(url):
        payload = {'api_key': API_KEY, 'url': url}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urllib.parse.urlencode(payload)
        return proxy_url

    # Main content - build URL, and soup content
    imdb_full_url = imdb_base_url + imdb_id
    r = requests.get(get_scrapeops_url(imdb_full_url)).content
    soup = BeautifulSoup(r, 'html.parser')
    print(f'[x]   ', end='')
    
    # Code from js section has json variables
    json_dict = json.loads( str( soup.findAll('script', {'type':'application/ld+json'})[0].text ))

    # Info - Movie title, year, parental content rating, poster url
    imdb_info_dict['title'] = json_dict['name']
    if 'contentRating' in json_dict:
        imdb_info_dict['MPAA'] = json_dict['contentRating'] 
    imdb_info_dict['poster_url'] = json_dict['image']
    imdb_info_dict['release_year'] = int( soup.find('span', {'id':'titleYear'}).a.text )
    imdb_info_dict['runtime'] = to_numeric( soup.find('time')['datetime'] )

    # Release date (from top header)
    date_string = soup.find('div', {'class':'title_wrapper'}).findAll('a')[-1].text.split(' (')[0]
    imdb_info_dict['release_date'] = date_string
    
    # Genres (up to 7)
    imdb_info_dict['genre'] = json_dict['genre']

    # Ratings - IMDb rating (and vote count), Metacritic
    imdb_info_dict['imdb_rating'] = float( json_dict['aggregateRating']['ratingValue'] )
    imdb_info_dict['num_imdb_votes'] = json_dict['aggregateRating']['ratingCount']

    # Metacritic score, if there is one
    if soup.find('div', {'class':'metacriticScore'}) != None:
        imdb_info_dict['metacritic'] = int( soup.find('div', {'class':'metacriticScore'}).span.text )

    # Reviews - Number of critic and public reviews (different than ratings/votes)
    num_review_list = soup.findAll('div',{'class':'titleReviewBarItem titleReviewbarItemBorder'})
    if num_review_list != []:
        reviews = num_review_list[0].findAll('a')
        if len(reviews) > 1:
            imdb_info_dict['num_critic_reviews'] = to_numeric( reviews[1].text )
        if len(reviews) > 0:
            imdb_info_dict['num_user_reviews'] = to_numeric( reviews[0].text )

    # Plots - long and short versions
    imdb_info_dict['plot_short'] = soup.find('div',{'class':'summary_text'}).text.strip()
    if 'Add a Plot' in imdb_info_dict['plot_short']:
        imdb_info_dict['plot_short'] = ''
    if soup.find('div',{'id':'titleStoryLine'}).div.p != None:
        imdb_info_dict['plot_long'] = soup.find('div',{'id':'titleStoryLine'}).div.p.span.text.strip()
    
    # Plot output
    print(f'[x]   ', end='')
    
    print(f"{(imdb_info_dict['title']+' ('+str(imdb_info_dict['release_year'])+')')[:100]:100} ", end='')
    time.sleep(random.randint(1,10) / 100)
    return imdb_info_dict

if __name__ == '__main__':
    print(imdb_scrape('tt0107290'))