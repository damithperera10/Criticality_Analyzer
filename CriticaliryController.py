from __future__ import print_function
import pickle
import csv
from nltk.corpus import stopwords
from CriticalityAlgo import extract_features
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

loadModal = pickle.load(open('CriticalityAnalysisModal.sav', 'rb'))
stopwords_set = set(stopwords.words("english"))


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id="AKIAJT3NTIISNIZ54VUQ",
                          aws_secret_access_key="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",
                          region_name="us-east-1",
                          endpoint_url="https://dynamodb.us-east-1.amazonaws.com"
                          )

table = dynamodb.Table('social_media_post')
response = []

try:
    response = table.scan(
        FilterExpression=Attr('accuracy').eq('high') | Attr('accuracy').eq('medium')
    )
except ClientError as e:
    print(e.response['Error']['Message'])

items = response['Items']
for i in items:
    data = i['post']
    newData = data
    data = data.lower()
    wordsSet = data.split()
    CleanData = [word for word in wordsSet
                 if 'http' not in word
                 and not word.startswith('@')
                 and not word.startswith('#')
                 and word != 'RT']
    words_without_stopwords = [word for word in CleanData if not word in stopwords_set]
    result = loadModal.classify(extract_features(words_without_stopwords))
    print(i['id'] + ' result is: ' + result)
    table.update_item(
        Key={
            'id': i['id'],
        },
        UpdateExpression="set criticality = :val",
        ExpressionAttributeValues={
            ':val': result
        },
        ReturnValues="UPDATED_NEW"
    )
    newDataFromResult = [{newData, result}]
    newDataFile = open('newData.csv', 'a')
    with newDataFile:
        writer = csv.writer(newDataFile)
        writer.writerows(newDataFromResult)


