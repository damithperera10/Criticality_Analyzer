import nltk
import csv
from nltk.corpus import stopwords
import pickle
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

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


# draw worldCloud
def wordcloud_draw(data, color='black'):
    words = ' '.join(data)
    cleaned_word = " ".join([word for word in words.split()
                             if 'http' not in word
                             and not word.startswith('@')
                             and not word.startswith('#')
                             and word != 'RT'
                             ])
    wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color=color,
                          width=2500,
                          height=2000
                          ).generate(cleaned_word)
    plt.figure(1, figsize=(13, 13))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()


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


# wordcloud_draw(w_features, 'black')

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in w_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


# wordcloud for high
# wordcloud_draw(train_high, 'red')

# wordcloud for medium
# wordcloud_draw(train_medium, 'black')

# wordcloud for low
#g wordcloud_draw(train_low, 'green')

# Training the Naive Bayes classifier
training_set = nltk.classify.apply_features(extract_features, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)

pickle.dump(classifier, open('CriticalityAnalysisModal.sav', 'wb'))
