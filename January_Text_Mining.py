# Imports
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import re
import spacy
import os
os.system('clear')

nlp = spacy.load('en_core_web_lg')

January_Tweets = pd.read_csv('January_Covid_Tweets.csv')

# Scraping Script leaves an unnamed columns in DF. I named it 'Tweets_Count' and then dropped it as it is not useful in the text mining process
January_Tweets = January_Tweets.drop(columns=['Tweet_Count'])
#print(January_Tweets.head(10))

# Pull the 'Tweet_Text' column and place in a variable to aid in text mining process
January_Tweet_Text = January_Tweets['Tweet_Text']
#print(January_Tweet_Text.head(10))

# Place tweet text into an array
January_Sentences = []
for word in January_Tweet_Text:
    January_Sentences.append(word)

#print(January_Sentences)

# Take the complete sentences and split them into individual words and place those words in a new array. This will aid in things like stemming
lines = []
for line in January_Sentences:
    words = line.split()
    for w in words:
        lines.append(w)

#print(lines)

# Use regex to remove punctuation
lines = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in lines]
#print(lines)

# If each word in the previous lines array is not equal to '' (essentially, if there is a word) append it to the new lines array. This should remove any empty strings
lines2 = []
for word in lines:
    if word != '':
        lines2.append(word)

#print(lines2)

stemmer = SnowballStemmer(language = 'english')
stem = []
for word in lines2:
    stem.append(stemmer.stem(word))

#print(stem)

# Remove all stop words
stem2 = []
for word in stem:
    if word not in nlp.Defaults.stop_words:
        stem2.append(word)

#print(stem2)

# Place the stem2 array into a new dataframe for future analysis
stem_df = pd.DataFrame(stem2)
stem_df = stem_df[0].value_counts()
#print(stem_df.head(5))

# Frequency Distribution
from nltk.probability import FreqDist
frequency = FreqDist()

for words in stem_df:
    frequency[words] += 1

#print(frequency)

# Visualizations
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import seaborn as sea

# Top 25 Words Used
stem_df_top_25 = stem_df[:25]
#print(stem_df_top_25)

# plt.figure(figsize = (10, 5))
# sea.barplot(stem_df_top_25.values, stem_df_top_25.index, alpha = 0.8)
# plt.title('Top 25 Words Used From January 2020')
# plt.ylabel('Word From Tweet', fontsize = 12)
# plt.xlabel('Word Count', fontsize = 12)
# plt.show()

from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
nlp.max_length = 2000000

def show_ents(doc):
    if doc.ents:
        for ent in doc.ents:
            print(ent.text + '-' + ent.label_ + '-' + str(spacy.explain(ent.label)))

str1 = " "
stem2 = str1.join(lines2)
stem2 = nlp(stem2)
label = [(X.text, X.label_) for X in stem2.ents]
df1 = pd.DataFrame(label, columns = ['Word', 'Entity'])
df2 = df1.where(df1['Entity'] == 'ORG')
df2 = df2['Word'].value_counts()

# df = df2[:14,]
# plt.figure(figsize = (10, 5))
# sea.barplot(df.values, df.index, alpha = 0.8)
# plt.title('Organizations Discussed in January 2020')
# plt.ylabel('Word from Tweet', fontsize = 12)
# plt.xlabel('Word Count', fontsize = 12)
# plt.show()


# Top People Mentioned
str1 = " "
stem2 = str1.join(lines2)
stem2 = nlp(stem2)
label = [(X.text, X.label_) for X in stem2.ents]
df3 = pd.DataFrame(label, columns = ['Word', 'Entity'])
df3 = df3.where(df3['Entity'] == 'PERSON')
df3 = df3['Word'].value_counts()

df = df3[:15,]
plt.figure(figsize = (10, 5))
sea.barplot(df.values, df.index, alpha = 0.8)
plt.title('Top People Discussed in January 2020')
plt.ylabel('Person Mentioned', fontsize = 12)
plt.xlabel('Word Count', fontsize = 12)
plt.show()