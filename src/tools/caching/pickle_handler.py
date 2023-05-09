import pickle
import os
import sys
import configparser

import boto3
from botocore.exceptions import ClientError

configObj = configparser.ConfigParser()
configObj.read("config.ini")
use_aws = configObj.getboolean("aws","use")

class PickleCachingHandler:
    def __init__(self,filename,config=None):
        if config is None:
            configObj = configparser.ConfigParser()
            configObj.read("config.ini")
            self.use_aws = configObj.getboolean("aws", "use")
        else:
            self.use_aws = config.getboolean("aws", "use")

        self.filename = filename
        if self.use_aws:
            session = boto3.Session(
                aws_access_key_id=configObj["aws"]["aws_access_key_id"],#'<your_access_key_id>',
                aws_secret_access_key=configObj["aws"]["aws_secret_access_key"]
            )

            s3 = session.resource('s3')
            self.aws_obj = s3.Object(configObj["aws"]["aws_bucket_name"],self.filename)

    def get(self,return_if_none=None):
        if self.use_aws:
            try:
                data = self.aws_obj.get()['Body'].read()
                return  pickle.loads(data)
            except ClientError as ex:
                return return_if_none
            return return_if_none
        else:

            if not os.path.isfile(self.filename):
                return return_if_none
            else:
                if os.path.getsize(self.filename)  > 0 :
                    with open(self.filename,"rb") as f:
                        content  = pickle.load(f)
                    return content
                else:
                    return return_if_none
    def store(self,data):
        if data is None : return
        if sys.getsizeof(data)  < 1: return
        if self.use_aws:
            self.aws_obj.put(Body=data)
        else:
            os.system("mkdir -p " + "/".join(self.filename.split("/")[:-1]))
            with open(self.filename,"wb") as f:
                pickle.dump(data,f)
