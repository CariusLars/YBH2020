import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import nltk
from nltk.corpus import stopwords

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

path = 'google_credentials.json' 
client = language.LanguageServiceClient.from_service_account_json(path)

nltk.download('stopwords')
stop_words=set(stopwords.words("german"))
df_top10 = pd.read_excel('top_10_words.xls')

def preprocess(text):
    text = text.lower()
    text = text.replace(r'[^\w\s]+', '')
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def get_score(tokens):
    score = dict.fromkeys(df_top10.columns, 0)
    for j in df_top10.columns:
        for l, l_in in zip(list(df_top10[j]), list(df_top10.index)):
            if l in tokens:
                score[j] += 10-l_in
    category = (max(score, key=score.get))
    score = score[max(score, key=score.get)]
    return score, category

def google_sentiment(text):
    # Score is positive or negative sentiment
    # Magnitude is how much the text displays that
    document = language.types.Document(
            content=text,
            type=language.enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    if (score <= 0.0):
        ex_negative = True
    else:
        ex_negative = False
    return ex_negative

def packaged_results(id, timestamp, message, user_name, contact_details):  #user_id, etc just given as examples
    category_score, category = get_score(preprocess(message))
    extreme_negative = google_sentiment(message)
    return {'id':id, 'timestamp':timestamp,'user_name':user_name, 'message': message, 'category': category, 'category_score': category_score, 'extreme_negative': extreme_negative}