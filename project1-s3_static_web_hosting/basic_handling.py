from email.policy import Policy
import boto3
import click

from pathlib import Path

# #custom session retrieves all the values of the profile as well
# session=boto3.Session(profile_name="diego")

# s3=session.resource('s3')

# for bucket in s3.buckets.all():
#     print(bucket.name)
# ##or
# # print(help(s3))

# #creating new bucket
# new_buck=s3.create_bucket(Bucket="testing222541678")
# print(new_buck)
# # new_buck.upload_file('filename', 'keyname', ExtraArgs={'ContentType': 'text/html'})

# #creating policies for the bucket
# policy='''
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Sid": "PublicReadGetObject",
#             "Effect": "Allow",
#             "Principal": "*",
#             "Action": "s3:GetObject",
#             "Resource": "arn:aws:s3:::%s/*"  
#         }
#     ]
# }
# ''' % new_buck.name


# #change bucketname
# print(policy)
# policy=policy.strip()  #to remove the firs line
# print(policy)

# # putting the policies into the bucket 
# pol= new_buck.Policy()
# print(type(pol))
# pol.put(Policy=policy)

# #adding website configuration into the same bucket 
# ws = new_buck.Website() 
# ws.put(WebsiteConfiguration={
#     'ErrorDocument': {
#         'Key': 'error.html'
#     },
#     'IndexDocument': {
#         'Suffix': 'index.html'
#     }
# })

# url = 'http://%s.s3-website.us-east-1.amazonaws.com'% new_buck.name

# print(s3.region)

# for bucket in s3.buckets.all():
#     print(bucket.name)

pathname="project1-s3_static_web_hosting/bloggingtemplate"
path=Path(pathname)
print(type(path))
print(path)
print(path.resolve())
print(list(path.iterdir()))
print()
path.is_dir()       #returns true if its a directory and false if not
path.is_file()      #vice-versa

def handle_directory(targetdir):
    for p in targetdir.iterdir():
        if p.is_dir(): handle_directory(p)      #recursive functions
        if p.is_file(): print(p.as_posix())     #we need posix system for the s3 bucket
        
handle_directory(path)

#for linux based system only
# or if user have given ~ symbol then we can use expand user
# pathname="~/home/bloggingtemplate"
# path=Path(pathname)
# path.expanduser()   
# handle_directory(path.expanduser())

root='C:/Users/DEREK/Desktop/python/project1-s3_static_web_hosting/bloggingtemplate'
pathname='C:/Users/DEREK/Desktop/python/project1-s3_static_web_hosting/bloggingtemplate/assets/css/animate.css'

path=Path(pathname)
print(path.relative_to(root))   #it will cut out the extra path here

def handle_directory(targetdir):
    for p in targetdir.iterdir():
        if p.is_dir(): handle_directory(p)      #recursive functions
        if p.is_file(): print(f"Path: {p} \n Key: {p.relative_to(root)}")
        
handle_directory(Path(root))

from pprint import  pprint
