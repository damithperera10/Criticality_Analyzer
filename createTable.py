from __future__ import print_function  # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id="AKIAJT3NTIISNIZ54VUQ",
                          aws_secret_access_key="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",
                          region_name="us-east-1",
                          endpoint_url="https://dynamodb.us-east-1.amazonaws.com"
                          )

dynamoTable = dynamodb.Table('social_media_post')
dynamoTable.put_item(
    # Item={
    #     'id': '0001',
    #     'post': 'I feel for these people deeply. They can not drink their water, bath in it or even cook with it. We here in Indiana have been steady collecting water and sending it to them on truck daily just so they can drink water. Having the amounts of lead they do in their water supply is tragic. Clean water should be available for these people.',
    #     'accuracy': 'high'
    # },
    # Item={
    #     #     'id': '0002',
    #     #     'post': 'It is being reported that there is a terrorist attack, or multiple attacks, in Brussels, the capital of Belgium. At least 34 are dead and 170 wounded. It is reported that at leas three explosions went off, one of which at the airport. CNN has details and video here.',
    #     #     'accuracy': 'medium'
    #     # }
    # Item={
    #     'id': '0003',
    #     'post': 'There is flooding situation and most of the people are rescue and safe, people able to care others and gave attention to help the them.',
    #     'accuracy': 'high'
    # },
    # Item={
    #     'id': '0004',
    #     'post': 'All 62 people on board have been killed, officials have said.Initial reports are that visibility was an issue, and it\'s not thought to be terror related.',
    #     'accuracy': 'medium'
    # },
    # Item={
    #     'id': '0005',
    #     'post': '27 people died on the spot and 2 others succumbed to their injuries in hospital later as tragedy hit big time in South Indian state of Andhra Pradesh. People are taking a holy dip in river Godavari, India\'s second biggest river for which a religious festival is celebrated. Despite huge arrangements and mock drills ahead of the mega ritual, people still died in a stampede as the crowd was said to have been detained to allow the state\'s chief minister to take a holy dip first.',
    #     'accuracy': 'low'
    # },
    # Item={
    #     'id': '0007',
    #     'post': 'According to this Xinhua report, the boat sank after being caught in a cyclone while steaming upriver. The AP reports that a total of 10 people - including the ships captain and engineer - have been rescued so far though ongoing rescue operations are being hampered by strong winds and heavy rain.',
    #     'accuracy': 'high'
    # },
    Item={
        'id': '0008',
        'post': 'the authorities late yesterday confirmed there were no deaths during the terror attack. However there is still independent verification of any of the reports. Meanwhile Capital FM has reported that one police officer injured in the attack died today in hospital.',
        'accuracy': 'medium'
    }

)
