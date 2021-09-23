import boto3

class ClientLocator:        #class used to create a new session for clients
    def __init__(self,client):
        self._client= boto3.client(client,region_name="us-east-1")
    
    def get_client(self):
        return self._client
    

class EC2Client(ClientLocator): #subclass of the above class
    def __init__(self):
        super().__init__('ec2')   #creating a client session for the ec2 class in here
        
    
class S3Client(ClientLocator):
    def __init__(self):
        super().__init__('s3')      #creating a client session for s3 class in here
        
    
    