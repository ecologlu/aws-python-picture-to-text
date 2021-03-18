import json
import boto3
import os
import urllib.parse
import re
print('Loading function')

s3 = boto3.client('s3')

# Amazon Textract client
textract = boto3.client('textract')

def getTextractData(bucketName, documentKey):
    print('Loading getTextractData')
    # Call Amazon Textract
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucketName,
                'Name': documentKey
            }
        })
        
    detectedText = ''

    # Print detected text
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            detectedText += item['Text'] + '\n'
            
    return detectedText
    
def writeTextractToS3File(textractData, bucketName, createdS3Document):
    print('Loading writeTextractToS3File')
    generateFilePath = os.path.splitext(createdS3Document)[0] + '.txt'
    s3.put_object(Body=textractData, Bucket=bucketName, Key=generateFilePath)
    print('Generated ' + generateFilePath)

def serial_finder(myline):
    new_string = re.sub("[^0-9a-zA-Z/]+", " ", myline)
    new_string = new_string.split()

    for index, element in enumerate(new_string):
        if (len(element)) == 10:
            if (element.startswith("INC") or element.startswith(
                    "CFT") or element.isnumeric() or element.isupper() == False):
                continue
            sncheck = False
            testindex = index - 5
            for i in range(testindex, index):
                if ("ser" in new_string[i].lower() or "s/n" in new_string[i].lower() or "sn" in new_string[i].lower()):
                    sncheck = True
            if (sncheck == True):
                return new_string[index] + "\n"

def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        detectedText = getTextractData(bucket, key)
        detectedText2 = serial_finder(detectedText)
        writeTextractToS3File(detectedText2, bucket, key)
        
        return 'Processing Done!'

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
