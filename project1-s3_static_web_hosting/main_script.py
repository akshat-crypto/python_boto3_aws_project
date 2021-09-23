

from bucket import BucketManager
import mimetypes
from pathlib import Path
import boto3
import click
import util



#custom session retrieves all the values of the profile as well
# session=boto3.Session(profile_name="diego")

# bucket_manager=BucketManager(session)

# s3=session.resource('s3')   #to connect with the s3 resource in here

session=None
bucket_manager=None
@click.group()
@click.option("--profile",default=None, help="Use a given AWS profile")
def cli(profile):
    global bucket_manager,session
    "Website Functions main decorator group "
    session_cfg={}
    if profile:
        session_cfg['profile_name']=profile
    # session=boto3.Session(profile_name="diego") #to get the profile value as an argument from the user
    session=boto3.Session(**session_cfg)    #this method is called glob and it will unrap the dictionary key value objs
    bucket_manager=BucketManager(session)
    
    


#now this function will work as the command options from the cli
@cli.command("list-bucket-objects") #one command in the cli group to get bucket object lists
@click.argument('bucket')
def list_bucket_objects(bucket):
    "Lists all the bucket objects"
    # for obj in s3.Bucket(bucket).objects.all():
    for obj in bucket_manager.all_objects(bucket):
        print(obj)
    

# @click.command("list-buckets")
@cli.command("list-buckets")
def list_buckets():
    "List all s3 buckets"
    # for bucket in s3.buckets.all():
    for bucket in bucket_manager.all_buckets():
        print("Bucket Name is: ", bucket.name)
    
    
@cli.command("configure-bucket")
@click.argument("bucket")
def config_bucket(bucket):
    "Create and configure s3 bucket name"
    #initializing or creating the bucket
    s3_buck=bucket_manager.init_bucket(bucket)
    
    bucket_manager.set_policy(s3_buck)
    #creates the policy to attach to this bucket
    
    bucket_manager.configure_website(s3_buck)
    #adding website configuration into the same bucket 
    return


@cli.command('sync')
@click.argument('pathname',type=click.Path(exists=True))    
@click.argument('bucketname')
def sync(pathname,bucketname):
    "Sync contents of Pathname to Bucket: Enter Pathname and Bucket names"
    
    bucket_manager.sync(pathname,bucketname)
    print(BucketManager.get_bucket_url(bucket_manager.s3.Bucket(bucketname)))
    #to get the absolute path the user entered
    

if __name__=='__main__':
    # print("Main Module")
    # list_buckets()
    cli()
    # print(session.region_name)