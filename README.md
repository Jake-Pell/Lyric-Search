# Lyric Search
This is a Python based tool that can be used to search for specific words or phrases within the lyrics of any songs in a given playlist. For example, you can enter a playlist and set the search for "Maryland." 
Then, the program will output any songs in the playlist that contain "Maryand" anywhere in the lyrics.

### Usage
You will need to obtain a free key for the [Genius API](https://docs.genius.com/)
1. Clone the repo
   ```
   git clone https://github.com/Jake-Pell/Lyric-Search.git
   ```
2. Install the required dependencies
   ```
   pip install -r requirements.txt
   ```
3. Create a .env file and enter your API key
   
    ```
   GENIUS_API_KEY = 'YOUR_API_KEY'
    ```

4. Populate `songs.txt` with the playlist of songs that you wish to search. The format for the file is `artist - title` <br>
   You can easily convert any Spotify playlist into this format using [this](https://www.chosic.com/spotify-playlist-exporter/) free online tool.

5. Add your desired search parameters to `search.txt`. Each line of this file will be a different phrase that is searched for in the playlist.
   
6. Run the program
   ```
   python LyricSearch.py
   ```

### Future Improvements
I am planning to integrate the Spotify API to allow users to simply enter the link to their playlist, rather than add the songs to a text file. The Spotify API does not provide lyrics, so it will still be necessary to search for the songs using the Genius API.

