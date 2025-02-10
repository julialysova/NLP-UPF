#python -m spacy download en_core_web_md
#python -m spacy download ru_core_news_md
import re
from collections import Counter

from math import log
import pandas as pd

import spacy
import matplotlib.pyplot as plt
import seaborn as sns


## FUNCTIONS
# Function for saving scrapped lyrics to a file for further usage
def save_lyrics_to_file(lyrics, file):
    with open(file, 'w', encoding='utf-8') as output_file:
        for song_name, lyric_text in lyrics.items():
            output_file.write(f"--- {song_name} ---\n")  # Song header
            output_file.write(lyric_text)
            output_file.write("\n\n")
    print(f"Lyrics saved to {file}")


# Function for reading the file with the lyrics
def read_lyrics_as_dictionary(filename):
    lyrics_dict = {}  # Dictionary to store song names and lyrics
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()  # Read the entire file content
        # Split by song headers
        song_sections = content.split('--- ')[1:]

        for section in song_sections:  # Iterate over each song section
            # Split each section into song name and lyrics
            parts = section.split(' ---\n', 1) # Split songs by their headings
            if len(parts) == 2:  # Ensure we have both song name and lyrics
                song_name, lyrics = parts  # Unpack into song name and lyrics
                lyrics_dict[song_name] = lyrics.strip() # Adding song name as key and lyrics as value, deleting trailing spaces

    return lyrics_dict


## KENDRICK ANALYSIS
# Creating an NLP object for English text processing
nlp = spacy.load("en_core_web_md")

# Reading file to lyrics_dictionary
lyrics_dictionary = read_lyrics_as_dictionary('kendrick_lamar_lyrics.txt')


# PROCESSING
# Creating a list for lyrics texts
kendrick_songs = []

# Deletion of tags and metadata in brackets
for song, text in lyrics_dictionary.items():
  text = re.sub("[\[<\(\{].*?[\]>\)\}]\n", "", text) # Deleting all the tags within the brackets
  text = re.sub("<.*?>", "", text) # Deleting the rest of html tags
  text = re.sub("\+", "", text) # Deleting the rest of html tags
  text = re.sub("[:\w\n\s\/\-&,#\'\?]+Typed\sby:\s\\b.+\\b", "", text) # Deleting the introductory part, which is not lyrics
  text = re.sub("\s+", " ", text) # Deleting extra spaces
  if text not in kendrick_songs: # Deleting duplicates
    kendrick_songs.append(text) # Adding the lyrics to the list

print(kendrick_songs[80])
# Print all song names
print("Number of Kendrick's songs:", len(kendrick_songs))

# Joining all the song in a text
kendrick_songs_joined = " ".join(kendrick_songs)
# Processing the text with the NLP object to get info on all the tokens
doc = nlp(kendrick_songs_joined)

# Putting all the lemmas from the list to one list for further counting
lemmas = [token.lemma_.lower() for token in doc if re.search(r'[a-zA-Z]', token.text) and not "/" in token.text  and not ")" in token.text] 
# lemma should not be a punctuation, space, or contain special symbol as "+"

# Using Counter for getting a number of occurence of each lemma
counted = Counter(lemmas)

print("Number of types in Kendrick Lamar's lyrics:", len(counted.keys()))
print("Most common tokens:")
print(counted.most_common(10))


# Creating a new dictionary to keep not only the number of each lemma's occurences, but also its length in letters
new_dict = {}
i = 1

for item in counted.most_common(): # Iterating over items in previous dict
  length = len(item[0]) # Counting the length of the lemma
  log_val = log(item[1]+1)
  new_dict[item[0]] = [length, item[1], log_val, i] # adding the length to the values list
  i += 1



# VISUALIZATION OF LEMMAS DISTRIBUTION PER LENGTH
# Group words by length and keep only the most frequent per length
word_groups = {}
for word, (length, freq, logfreq, _) in new_dict.items():
    if length not in word_groups or freq > word_groups[length][1]:
        word_groups[length] = (word, freq, logfreq)  # Store word, frequency, and logfreq

# Convert dictionary to DataFrame
df = pd.DataFrame.from_dict(new_dict, orient='index', columns=["length", "frequency", "logfreq", "rank"])
df = df.reset_index().rename(columns={"index": "word"})  # Add 'word' as a column

# Filter df2 to include only the most frequent word per length
df_labels = pd.DataFrame(word_groups.values(), columns=["word", "frequency", "logfreq"])
df_labels["length"] = list(word_groups.keys())  # Add back the lengths

# Plot using scatterplot
plt.figure(figsize=(12, 6))
sns.scatterplot(x="length", y="logfreq", data=df, color="firebrick", marker="o", alpha=0.9)

# Add labels only for the most frequent word per length
for _, row in df_labels.iterrows():
    plt.annotate(
        row["word"], 
        (row["length"], row["logfreq"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=7,
        ha='right',
        rotation=17
    )

# Customize ticks and grid
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.xticks(fontsize=10, ticks=range(0,26))
plt.yticks(fontsize=10)
plt.xlabel("Word Length", fontsize=12)
plt.ylabel("Frequency (log scale)", fontsize=12)
plt.title("Zipf's Law for Lemmas in Kendrick Lamar's lyrics", fontsize=14)
plt.show()
print("Mean length of lemmas in Kendrick Lamar's lyrics:", df["length"].mean())


## OXXXYMIRON ANALYSIS
# Reading file to lyrics_dictionary
lyrics_dictionary2 = read_lyrics_as_dictionary('oxxxymiron_lyrics.txt')

# PROCESSING
# Creating a list for lyrics texts
oxxxy_songs = []

# Deletion of tags and metadata in brackets
for song, text in lyrics_dictionary2.items():
  text = re.sub("\[.*?\]", "", text) # Deleting all the tags within the brackets
  text = re.sub(".*lyrics", "", text) # Deleting the introductory part, which is not lyrics
  text = re.sub("\n|°|ð", " ", text) # Deleting extra symbols
  if text not in oxxxy_songs: # Deleting duplicates
    oxxxy_songs.append(text) # Adding the lyrics to the list

print(oxxxy_songs[80])

print("Number of Oxxxymiron's songs: ", len(oxxxy_songs))

# Creating an NLP object for Russian text processing
nlp_ru = spacy.load("ru_core_news_md")

# Joining all the song in a text
oxxxy_songs_joined = " ".join(oxxxy_songs)
# Processing the text with the NLP object to get info on all the tokens
doc2 = nlp_ru(oxxxy_songs_joined)

# Putting all the lemmas from the list to one list for further counting
lemmas2 = [token.lemma_.lower() for token in doc2 if re.search(r'[а-яА-ЯёЁ]', token.text)]
# lemma should contain Russian alphabet letters

# Using Counter for getting a number of occurence of each lemma
counted2 = Counter(lemmas2)

print("Number of types in Oxxxymiron's lyrics:", len(counted2.keys()))
print("Most common tokens:")
print(counted2.most_common(10))

# Creating a new dictionary to keep not only the number of each lemma's occurences, but also its length in letters
new_dict2 = {}
i = 1

for item in counted2.most_common(): # Iterating over items in previous dict
  length = len(item[0]) # Counting the length of the lemma
  log_val = log(item[1]+1)
  new_dict2[item[0]] = [length, item[1], log_val, i] # adding the length to the values list
  i += 1


## VISUALIZATION
# Group words by length and keep only the most frequent per length
word_groups2 = {}
for word, (length, freq, logfreq, _) in new_dict2.items():
    if length not in word_groups2 or freq > word_groups2[length][1]:
        word_groups2[length] = (word, freq, logfreq)  # Store word, frequency, and logfreq

# Convert dictionary to DataFrame
df2 = pd.DataFrame.from_dict(new_dict2, orient='index', columns=["length", "frequency", "logfreq", "rank"])
df2 = df2.reset_index().rename(columns={"index": "word"})  # Add 'word' as a column

# Filter df2 to include only the most frequent word per length
df_labels = pd.DataFrame(word_groups2.values(), columns=["word", "frequency", "logfreq"])
df_labels["length"] = list(word_groups2.keys())  # Add back the lengths

# Plot using scatterplot
plt.figure(figsize=(12, 6))
sns.scatterplot(x="length", y="logfreq", data=df2, color="firebrick", marker="o", alpha=0.9)

# Add labels only for the most frequent word per length
for _, row in df_labels.iterrows():
    plt.annotate(
        row["word"], 
        (row["length"], row["logfreq"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=7,
        ha='right',
        rotation=17
    )

# Customize ticks and grid
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.xticks(fontsize=10, ticks=range(0,26))
plt.yticks(fontsize=10)
plt.xlabel("Word Length", fontsize=12)
plt.ylabel("Frequency (log scale)", fontsize=12)
plt.title("Zipf's Law for Lemmas in Oxxxymiron's lyrics", fontsize=14)
plt.show()

print("Mean length of lemmas in Oxxxymiron's lyrics:", df2["length"].mean())