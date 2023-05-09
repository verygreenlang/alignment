import json
import os
import configparser
import boto3
from botocore.exceptions import ClientError



class FileCachingHandler:
    def __init__(self,filename,config=None):
        if config is None :
            configObj = configparser.ConfigParser()
            configObj.read("config.ini")
            self.use_aws = configObj.getboolean("aws", "use")
        else:
            self.use_aws = config.getboolean("aws", "use")
        self.filename = filename

    def get(self,return_if_none=None):
        return return_if_none
    def store(self,path_to_file):
        if self.use_aws:
            bucket = self.configObj["aws"]["aws_bucket_name"]
            s3 = boto3.client('s3',
                              aws_access_key_id=self.configObj["aws"]["aws_access_key_id"],
                              aws_secret_access_key=self.configObj["aws"]["aws_secret_access_key"],
                              )
            try:
                s3.head_object(Bucket=bucket, Key=path_to_file)
            except ClientError:
                s3.upload_file(path_to_file, bucket, path_to_file)
