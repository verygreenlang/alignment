import json
import os
import configparser
import boto3
from botocore.exceptions import ClientError



class JsonCachingHandler:
    def __init__(self,filename,config=None):
        if config is None :
            configObj = configparser.ConfigParser()
            configObj.read("config.ini")
            self.use_aws = configObj.getboolean("aws", "use")
        else:
            self.use_aws = config["aws"]["use"]

        self.filename = filename
        if self.use_aws:
            session = boto3.Session(
                aws_access_key_id=configObj["aws"]["aws_access_key_id"],#'<your_access_key_id>',
                aws_secret_access_key=configObj["aws"]["aws_secret_access_key"]
            )

            s3 = session.resource('s3')
            self.aws_obj = s3.Object(configObj["aws"]["aws_bucket_name"],self.filename)
    def get(self,return_if_none=None):
        if not self.use_aws:
            if not os.path.isfile(self.filename):
                return return_if_none
            with open(self.filename,"rb") as f:
                return json.load(f)
        else:
            try:
                return json.loads(self.aws_obj.get()['Body'].read().decode('utf-8'))
            except ClientError as ex:
                return return_if_none
            return return_if_none
    def store(self,data):
        if not  self.use_aws:
            with open(self.filename,"w") as f:
                json.dump(data,f)
        else:
            self.aws_obj.put( Body=json.dumps(data))
