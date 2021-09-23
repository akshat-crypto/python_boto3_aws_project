# -*- coding: utf-8 -*- 
#defines the coding format here
from ast import With
from hashlib import md5
import mimetypes
from pathlib import Path
from pprint import pprint
import boto3

# from cv2 import reduce
from botocore.exceptions import ClientError
import mimetypes
import util
from functools import reduce
"""Class for S3 buckets."""

class BucketManager:
    """Manages S3 bucket."""
    CHUNK_SIZE=8388608
    
    def __init__(self,session):
        """Create a BucketManager object."""
        # self.session =session #for the session location consraint value
        self.s3 = session.resource('s3')
        self.manifest = {}
        self.transfer_config=boto3.s3.transfer.TransferConfig(
            multipart_chunksize=self.CHUNK_SIZE,
            multipart_threshold=self.CHUNK_SIZE,
        )
        
        
    def get_region_name(self,bucket):
        """Get the bucket's rgion name."""
        bucket_location= self.s3.meta.client.get_bucket_location(Bucket=bucket.name)    #check into the documentation
        return bucket_location["LocationConstraint"]
        
    def get_bucket_url(self,bucket):
        """Get the website URL for this bucket."""
        return "http://{}.{}".format(bucket.name,util.get_endpoint(self.get_region_name(bucket)).host)
    
    def all_buckets(self):
        """Get an iterator for all buckets."""
        return self.s3.buckets.all()
    
    def all_objects(self,bucket_name):
        """Get an iterator for all objects in given bucket list"""
        return self.s3.Bucket(bucket_name).objects.all()
    
    def init_bucket(self,bucket_name):
        s3_buck=None
        try:
            s3_buck=self.s3.create_bucket(Bucket=bucket_name) #region name is optional now
        except ClientError as e:
            print(e.response)
            if e.response['Error']['Code'] == "BucketAlreadyOwnedByYou":
                s3_buck = self.s3.bucket(bucket_name)
            else:
                raise e
        return s3_buck
    
    def set_policy(self,bucket):
        policy='''
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::%s/*"  
                }
            ]
        }
        ''' % bucket.name   #changes the name in the policy here
        # s3_buck.name
        
        #adding bucket policies for public access
        policy=policy.strip()
        # pol= s3_buck.Policy()
        pol= bucket.Policy()
        pol.put(Policy=policy)
    
    def configure_website(self, bucket):
        bucket.Website().put(WebsiteConfiguration={
                'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        })
        #     ws = s3_buck.Website() 
        # ws.put(WebsiteConfiguration={
        #     'ErrorDocument': {
        #         'Key': 'error.html'
        #     },
        #     'IndexDocument': {
        #         'Suffix': 'index.html'
        #     }
        # })
        
    
    def load_manifest(self,bucket):
        """Load manifest for caching purpose"""
        paginator=self.s3.meta.client.get_paginator('list_object_v2')
        for page in paginator.paginate(Bucket=bucket.name):
            for obj in page.get('Contents', []):
                self.manifest[obj['Key']] = obj['ETag']
                pprint(obj)
        
    @staticmethod        
    def has_data(data):
        """Generat md5 hash for data."""
        hash=md5()
        hash.update(data)
        return hash
    
    def gen_etag(self,path):
        """Generate etag for file."""
        hashes=[]
        hash=None
        
        with open(path, 'rb') as f:
            while True:
                data=f.read(self.CHUNK_SIZE)
                
                if not data:
                    break
                
                hashes.append(self.hash_data(data))
            
            if not hashes:
                return     
            elif len(hashes) == 1:
                # hash = self.hash_data(data)
                # return '"{}"'.format(hash.hexdigest())
                return '"{}"'.format(hashes[0].hexdigest())
            else:
                hash=self.hash_data(reduce(lambda x,y: x + y,  (h.digest() for h in hashes)))
                return '"{}-{}"'.format(hash.hexdigest(),len(hashes))
            
        
    # @staticmethod
    # def upload_files(bucket,path,key):
    def upload_files(self,bucket,path,key):     #can be use as static method because we dont need anything from the class in this
    # def upload_files(self,bucket,path,key):     #can be use as static method because we dont need anything from the class in this
    #also to change the content type according to the key we use mimetypes(media-type) library
        # content_type= mimetypes.guess_type(key)[0] or 'text/plain'  #we cant pass the none values if the type is not known
        
        # s3_bucket.upload_file(
        #     path,
        #     key,
        #     ExtraArgs={
        #         'ContentType': 'text/html'
        #     }
        # )
        content_type= mimetypes.guess_type(key)[0] or 'text/plain'  #we cant pass the none values if the type is not known
        
        # etag=self.gen_etag(path)
        # if self.manifest.get(key,'')==etag:
            # print("Skipping {}, etags match".format(key))
            # return
        
        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                # 'ContentType': 'text/html'
                'ContentType': content_type,
                
            },
            # Config=self.transfer_config
        )
    
    def sync(self,pathname,bucket_name):
        bucket=self.s3.Bucket(bucket_name)
        # self.load_manifest(bucket)
        root=Path(pathname).expanduser().resolve()  #first removes any ~ symbol and then resolves it 
        
        def handle_directory(targetdir):    #function can be defined in another function
            for p in targetdir.iterdir():
                if p.is_dir(): handle_directory(p)      #recursive functions
                # if p.is_file(): print(f"Path: {p} \n Key: {p.relative_to(root)}")
                if p.is_file(): self.upload_files(bucket,str(p),str(p.relative_to(root))) #passes the required args in string form
                

        handle_directory(root)  #calls the function with absolute path

