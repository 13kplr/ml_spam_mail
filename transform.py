import joblib
import email
import re
import string
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

rfc = joblib.load('./finalized_model.sav')
vectorizer = joblib.load('./vectorizer2.sav')


class email_to_clean_text1(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y=None): 
        return self
    def transform(self, X):
        text_list = []
        b = email.message_from_string(X)
        body = ""

        if b.is_multipart():
            for part in b.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                # skip any text/plain (txt) attachments
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # get body of email
                    break
        # not multipart - i.e. plain text, no attachments, keeping fingers crossed
        else:
            body = b.get_payload(decode=True) # get body of email
        #####################################################
        soup = BeautifulSoup(body, "html.parser") #get text from body (HTML/text)
        text = soup.get_text().lower()
        #####################################################
        text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE) #remove links
        ####################################################
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text, flags=re.MULTILINE) #remove email addresses
        ####################################################
        text = text.translate(str.maketrans('', '', string.punctuation)) # remove punctuation
        ####################################################
        text = ''.join([i for i in text if not i.isdigit()]) # remove digits
        ####################################################
        stop_words = stopwords.words('english')
        words_list = [w for w in text.split() if w not in stop_words] # remove stop words
        ####################################################
        words_list = [lemmatizer.lemmatize(w) for w in words_list] #lemmatization
        ####################################################
        words_list = [stemmer.stem(w) for w in words_list] #Stemming
        text_list.append(' '.join(words_list))
        result = ''.join(text_list)
        return result