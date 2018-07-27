import nltk
import csv
from nltk.corpus import stopwords
import pickle

data = []
with open('dataSet.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        data.append(row)

train_high = []
train_medium = []
train_low = []

for i in data:
    if i[1] == 'high':
        train_high.append(i[0])
    if i[1] == 'medium':
        train_medium.append(i[0])
    if i[1] == 'low':
        train_low.append(i[0])
tweets = []
stopwords_set = set(stopwords.words("english"))

for index, row in data:
    words_filtered = [e.lower() for e in index.split() if len(e) >= 3]
    words_cleaned = [word for word in words_filtered
                     if 'http' not in word
                     and not word.startswith('@')
                     and not word.startswith('#')
                     and word != 'RT']
    words_without_stopwords = [word for word in words_cleaned if not word in stopwords_set]
    tweets.append((words_without_stopwords, row))

# Extracting word features
def get_words_in_tweets(tweets):
    all = []
    for (words, criticality) in tweets:
        all.extend(words)
    return all


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    features = wordlist.keys()
    return features


w_features = get_word_features(get_words_in_tweets(tweets))


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in w_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


# Training the Naive Bayes classifier
training_set = nltk.classify.apply_features(extract_features, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)

pickle.dump(classifier, open('CriticalityAnalysisModal.sav', 'wb'))
