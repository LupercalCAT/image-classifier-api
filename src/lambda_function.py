import json
import boto3
import base64


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')

    http_method = event['httpMethod']

    if http_method == 'GET':
        doc_id = event['queryStringParameters'].get('doc_id')

        if doc_id:
            table = dynamodb.Table('image-classifier')

            try:
                # Fetch the document from DynamoDB
                response = table.get_item(Key={'doc_id': doc_id})
                return {
                    'statusCode': 200,
                    'body': json.dumps(response.get('Item', {}))
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': 'Error fetching document: ' + str(e)
                }
        else:
            return {
                'statusCode': 400,
                'body': 'Missing doc_id parameter'
            }

    elif http_method == 'POST':
        try:
            body = json.loads(event['body'])
            # Assuming the PDF content is sent base64-encoded in the 'pdf_data' field
            pdf_data = body['pdf_data']
            # Convert the base64 string back to bytes
            pdf_bytes = base64.b64decode(pdf_data)

            # Upload the PDF to S3
            s3.put_object(
                Bucket='image-classifier-mullins',
                Key='pdf_documents/document.pdf',  # replace with your desired object key
                Body=pdf_bytes,
                ContentType='application/pdf'
            )

            return {
                'statusCode': 200,
                'body': 'PDF uploaded successfully'
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': 'Error uploading PDF: ' + str(e)
            }

    else:
        return {
            'statusCode': 400,
            'body': 'Invalid HTTP method'
        }
