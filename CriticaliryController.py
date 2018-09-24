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
from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify

app = Flask(__name__)
api = Api(app)

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
                          aws_access_key_id="AKIAJ3G6N4MARQVO6JJA",
                          aws_secret_access_key="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",
                          region_name="us-east-1",
                          endpoint_url="https://dynamodb.us-east-1.amazonaws.com"
                          )

table = dynamodb.Table('social_media_post')


@app.route('/criticality/<string:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        response = table.scan(
            FilterExpression=Attr('id').eq(post_id)
        )
        item = response['Items']
        data = item[0]['post']
        new_data = data
        data = data.lower()
        words_set = data.split()
        clean_data = [word for word in words_set
                     if 'http' not in word
                     and not word.startswith('@')
                     and not word.startswith('#')
                     and word != 'RT']
        words_without_stopwords = [word for word in clean_data if not word in stopwords_set]
        result = loadModal.classify(extract_features(words_without_stopwords))

        table.update_item(
            Key={
                'id': item[0]['id'],
            },
            UpdateExpression="set criticality = :val",
            ExpressionAttributeValues={
                ':val': result
            },
            ReturnValues="UPDATED_NEW"
        )
        print(item[0]['id'] + ' result is: ' + result + ' and data base update successful.')
        new_data_from_result = [{new_data, result}]
        new_data_file = open('newData.csv', 'a')
        with new_data_file:
            writer = csv.writer(new_data_file)
            writer.writerows(new_data_from_result)

        return jsonify(item[0]['id'])
    except ClientError as e:
        print(e.response['Error']['Message'])


if __name__ == '__main__':
    print("Server is running on port 5002")
    app.run(port='5002')
