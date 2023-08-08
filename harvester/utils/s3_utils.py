import boto3

class S3SubtitleManager:
    def __init__(self, bucket_name):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name

    def subtitle_exists(self, video_id):
        file_key = f'youtube/{video_id}.txt'
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_key)
            return True
        except boto3.exceptions.botocore.exceptions.ClientError:
            return False

    def upload_subtitle(self, video_id, subtitle):
        file_key = f'youtube/{video_id}.txt'
        self.s3_client.put_object(Bucket=self.bucket_name, Key=file_key, Body=subtitle, ContentType='text/plain')
