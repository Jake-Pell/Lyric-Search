import requests
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GENIUS_API_KEY')

search_params = []

def main():
    getSearchParams('search.txt')
    song_matches = getSongs('songs.txt')
    print('\n----------------------------------------\n')
    print('Lyric Matches: \n')
    if not song_matches:
        print('None')
    else:
        for song in song_matches:
            print(f"{song['artist']} - {song['title']} [Matched: {song['matched_param']}]")
    print()

# Read search parameters from the file
# Each line of the file will be searched for in the lyrics of each song
def getSearchParams(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            search_params.append(line.lower().strip())


# Find data for all songs in the file
# Returns any songs that contain lyrics that match the search parameters
def getSongs(file_name):
    songs = []
    with open(file_name, 'r') as file:
        for line in file:
            if '-' not in line:
                continue
            line = re.sub(r'\(.*?\)', '', line) # Remove anything inside parentheses, makes the search results more reliable
            artist, title = line.strip().split('-', 1) 
            search_term = f'{title} {artist}'

            # API call
            genius_search_url = f'https://api.genius.com/search?q={search_term}&access_token={api_key}'
            response = requests.get(genius_search_url)
            if response.status_code != 200:
                print(f'Error searching for {search_term}')
                continue

            json_data = response.json()

            # Find the correct song from the search results
            # Add it to the return list if lyrics match the search parameters
            found_match = False
            for hit in json_data['response']['hits']:
                result = hit['result']
                hit_title = result['title'].lower().strip()
                hit_artist = result['primary_artist']['name'].lower().strip()

                if title.lower().strip() in hit_title and artist.lower().split(',')[0].strip() in hit_artist:
                    song_data = {
                        'title': result['title'],
                        'artist': result['primary_artist']['name'],
                        'url': result['url'],
                        'lyrics': getSongLyrics(result['url'])
                    }
                    lyrics_lower = song_data['lyrics'].lower()
                    for param in search_params:
                        if param in lyrics_lower:
                            song_data['matched_param'] = param
                            songs.append(song_data)
                            break
                    found_match = True
                    break

            if not found_match:
                print(f'Song could not be found: {search_term}')

    return songs

# Get lyrics from song URL
def getSongLyrics(song_url):
    song = requests.get(song_url)
    soup = BeautifulSoup(song.content, 'html.parser')
    lyrics_container = soup.select('div[class^="Lyrics__Container"], div[data-lyrics-container="true"]')
    
    if not lyrics_container:
        return 'Lyrics not found'
    
    lyrics = '\n'.join([container.get_text() for container in lyrics_container])
    return lyrics

main()
