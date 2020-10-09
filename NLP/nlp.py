import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

path = 'google_credentials.json' 
client = language.LanguageServiceClient.from_service_account_json(path)

nltk.download('stopwords')
df_top10 = pd.read_excel('top_10_words.xls')

def preprocess(text):
    text = text.lower()
    text = text.replace(r'[^\w\s]+', '')
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def get_score(tokens):
    score = dict.fromkeys(df_top10.columns, 0)
    for j, j_in in zip(df_top10.columns, list(df_top10.index)):
        for l in df_top10[j]:
            if l in tokens:
                score[j] += 10-j_in
    category = (max(score, key=score.get))
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
    if score > 2 & magnitude > 4:
        ex_negative = True
    return ex_negative

def packaged_results(text, user_id, etc):  #user_id, etc just given as examples
    score, category = get_score(preprocess(text))
    ex_negative = google_sentiment(text)
    return {'user_id':user_id, 'text': text, 'category': category, 'score': score, 'ex_negative': ex_negative}