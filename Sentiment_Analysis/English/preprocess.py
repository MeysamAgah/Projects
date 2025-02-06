# import necessary modules
import re
import string
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from autocorrect import Speller

# patterns to detect emojies and emoticons in text
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

def preprocess(text,
              lowercase=True,
              remove_number=True,
              remove_html=True,
              remove_url=True,
              remove_punctuation=True,
              remove_emoji=True,
              spell_correction=True,
              tokenize=True,
              remove_stopword=True,
              stemming=True):
  # lowercase
  text = text.lower()

  # remove numbers
  for i in "0123456789":
    text = text.replace(i, "")

  # remove html tags
  text = re.sub('<.*?>', '', text)

  # url remove
  text = re.sub(r'http\S +|https\S +|www\S', '', text)

  # remove punctuations
  text = text.translate(str.maketrans('', '', string.punctuation))

  # remove emoji
  text = emoji_pattern.sub(r'', text)

  # Spelling correction
  #text = TextBlob(text).correct().string
  spell = Speller(lang='en')
  text = spell(text)

  # Tokenizing words
  tokens = word_tokenize(text)

  # Removing stop words
  stop_words = set(stopwords.words('english'))
  filtered_text = [word for word in tokens if word.lower() not in stop_words]
  text = ' '.join(filtered_text)

  # Stemming words
  stemmer = PorterStemmer()
  stemmed_text = [stemmer.stem(word) for word in text.split()]
  text = ' '.join(stemmed_text)

  return text
