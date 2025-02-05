import requests
from bs4 import BeautifulSoup
import time

# Function for scraping song lyrics from ohhla.com
def scrape_ohhla_lyrics(base_url):
    # Fetch the main page
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all lyric links
    lyric_links = soup.find_all('a', href=lambda href: href and href.endswith('.txt'))

    # Dictionary to store lyrics
    lyrics_collection = {}

    # Base URL for constructing full links
    base_site = 'http://www.ohhla.com/'

    # Scrape each lyric
    for link in lyric_links:
        try:
            full_url = base_site + link['href']
            lyric_response = requests.get(full_url)

            # Use appropriate encoding
            lyric_response.encoding = 'ISO-8859-1'

            # Store lyrics with song name as key
            lyrics_collection[link.text] = lyric_response.text
        except Exception as e:
            print(f"Error scraping {link.text}: {e}")

    return lyrics_collection


# Function for scraping song lyrics from lyrics.az

def scrape_lyricsaz_lyrics(base_url):
    # Fetch the main page
    response = requests.get(base_url)   
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all song links
    lyric_links = soup.find_all('a', href=True)
    song_urls = [link['href'] for link in lyric_links if "/oxxxymiron/" in link['href'] and link['href'].endswith(".html")]

    # Dictionary to store lyrics
    lyrics_collection = {}

    # Scrape each song's lyrics
    for song_url in song_urls:
        try:
            time.sleep(1)  # Avoid overloading the server
            song_response = requests.get(song_url) # Accessing the webpage
            song_soup = BeautifulSoup(song_response.text, 'html.parser') # Parsing the webpage

            # Extract song title
            title_tag = song_soup.find("h1")
            song_title = title_tag.get_text(strip=True) if title_tag else "Unknown Song"

            # Extract lyrics (inside the main lyrics div)
            lyrics_div = song_soup.find("div", class_="position-relative song-lyrics-wrapper")
            lyrics_text = lyrics_div.get_text("\n", strip=True) if lyrics_div else "Lyrics not found"

            lyrics_collection[song_title] = lyrics_text

        except Exception as e:
            print(f"Error scraping {song_url}: {e}")

    return lyrics_collection


# Function for saving scrapped lyrics to a file for further usage
def save_lyrics_to_file(lyrics, file):
    with open(file, 'w', encoding='utf-8') as output_file:
        for song_name, lyric_text in lyrics.items():
            output_file.write(f"--- {song_name} ---\n")  # Song header
            output_file.write(lyric_text)
            output_file.write("\n\n")
    print(f"Lyrics saved to {file}")


# URL for Kendrick Lamar artist page
base_url = 'https://www.ohhla.com/YFA_kendricklamar.html'
# Sraping the lyrics
lyrics = scrape_ohhla_lyrics(base_url)
# Saving songs to a file
save_lyrics_to_file(lyrics, 'kendrick_lamar_lyrics.txt')



# URL for Oxxxymiron artist page
base_url2 = 'https://lyrics.az/oxxxymiron/allsongs.html'
# Sraping the lyrics
lyrics2 = scrape_lyricsaz_lyrics(base_url2)
# Saving songs to a file
save_lyrics_to_file(lyrics2, "oxxxymiron_lyrics.txt")