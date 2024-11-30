import boto3
import json
import requests
import os

dyn_resource = boto3.resource("dynamodb",region_name='us-east-1')
s3_client= boto3.client('s3')


def create_table(): #code adapted from https://docs.aws.amazon.com/code-library/latest/ug/dynamodb_example_dynamodb_CreateTable_section.html

     table_name = "login"
     params = {
         "TableName": table_name,
         "KeySchema": [
             {"AttributeName": "email", "KeyType": "HASH"}
         ],
         "AttributeDefinitions": [
             {"AttributeName": "email", "AttributeType": "S"}
         ],
         "ProvisionedThroughput": {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
     }

     table = dyn_resource.create_table(**params)
     table.wait_until_exists()
     return table


def create_subscribe_table():
    table_name = "subscription"
    params = {
        "TableName": table_name,
        "KeySchema": [
            {"AttributeName": "email", "KeyType": "HASH"},
            {"AttributeName": "title", "KeyType": "RANGE"}

        ],
        "AttributeDefinitions": [
            {"AttributeName": "email", "AttributeType": "S"},
            {"AttributeName": "title", "AttributeType": "S"}
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    }

    table = dyn_resource.create_table(**params)
    table.wait_until_exists()

def add_item(table): #code adapted from https://docs.aws.amazon.com/code-library/latest/ug/dynamodb_example_dynamodb_PutItem_section.html
     items = [
         {
         "email": "s3000000@student.rmit.edu.au",
         "password": "01010",
         "username": "AAA0"
     },
    {
         "email": "s3111111@student.rmit.edu.au",
         "password": "12345",
         "username": "ABC1"
     },
     {
         "email": "s3222222@student.rmit.edu.au",
         "password": "21345",
         "username": "DEF2"

     },
     {
         "email": "s3333333@student.rmit.edu.au",
         "password": "31245",
         "username": "GHI3"

     },
     {
         "email": "s3444444@student.rmit.edu.au",
         "password": "41235",
         "username": "JKL4"

     },
     {
         "email": "s3555555@student.rmit.edu.au",
         "password": "51234",
         "username": "MNO5"

     },
     {
         "email": "s3666666@student.rmit.edu.au",
         "password": "00000",
         "username": "PQR6"

     },
     {
         "email": "s3777777@student.rmit.edu.au",
         "password": "11111",
         "username": "STU7"

     },
     {
         "email": "s3888888@student.rmit.edu.au",
         "password": "22222",
         "username": "VWX8"

     },
     {
         "email": "s3999999@student.rmit.edu.au",
         "password": "33333",
         "username": "XYZ9"

     }]
     for item in items:
         table.put_item(Item=item)

def second_table():

     table_name = "music"
     params = {
         "TableName": table_name,
         "KeySchema": [
             {"AttributeName": "title", "KeyType": "HASH"},
             {"AttributeName": "artist", "KeyType": "RANGE"}
         ],
         "AttributeDefinitions": [
             {"AttributeName": "title", "AttributeType": "S"},
             {"AttributeName": "artist", "AttributeType": "S"}
         ],
         "ProvisionedThroughput": {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
     }
     table = dyn_resource.create_table(**params)
     table.wait_until_exists()
     return table

def data_load():
     with open('a1.json', 'r') as file:
         data = json.load(file)
         songs = data.get('songs', [])

         for item in songs:
            table = dyn_resource.Table('music')
            table.put_item(
                 Item={
                     'title':  item['title'],
                     'artist': item['artist'],
                     'year': item['year'],
                     'web_url': item['web_url'],
                     'image_url': item['img_url'],
                     }
             )

def download_upload_img(): #
         with open('a1.json', 'r') as file:
             data = json.load(file)
             songs = data.get('songs', [])

             for song in songs:
                 if song['img_url']:
                     img_download = requests.get(song['img_url']).content #adapted from https://www.geeksforgeeks.org/response-content-python-requests/
                     img_name = os.path.basename(song['img_url']) #adapted from https://www.geeksforgeeks.org/python-program-to-get-the-file-name-from-the-file-path/
                     with open(img_name, 'wb') as img_file:
                         img_file.write(img_download)
                         bucket_name='mybucket.newassign'
                         s3_client.create_bucket(Bucket=bucket_name)
                         s3_client.upload_file(img_name,bucket_name,img_name)

def main():
     new_table = create_table()
     print(f"Created table.")
     create_subscribe_table()
     add_item(new_table)
     second_table()
     print(f"Created music table")
     data_load()
     print(f"Data loaded into music")
     download_upload_img()
     print(f"image uploaded to bucket")

if __name__ == "__main__":
     main()