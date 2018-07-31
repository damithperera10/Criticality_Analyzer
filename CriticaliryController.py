import pickle
import csv
from nltk.corpus import stopwords
from CriticalityAlgo import extract_features

loadModal = pickle.load(open('CriticalityAnalysisModal.sav', 'rb'))

data = "The AP mentions that a total of 55 people were injured in the crash. However, federal authorities believe that as many as 62 were believed to be injured."
newData = data
data = data.lower()

wordsSet = data.split()
stopwords_set = set(stopwords.words("english"))

CleanData = [word for word in wordsSet
             if 'http' not in word
             and not word.startswith('@')
             and not word.startswith('#')
             and word != 'RT']
words_without_stopwords = [word for word in CleanData if not word in stopwords_set]

result = loadModal.classify(extract_features(words_without_stopwords))

newDataFromResult = [{newData, result}]
newDataFile = open('newData.csv', 'a')
with newDataFile:
    writer = csv.writer(newDataFile)
    writer.writerows(newDataFromResult)
print(result)
