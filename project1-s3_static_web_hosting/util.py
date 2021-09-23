#every s3 bucket have different endpoints in it so what we do is we will copy the 
#resource file in here and use them accordingly
#https://docs.aws.amazon.com/general/latest/gr/s3.html -link for the files

from collections import namedtuple

Endpoint=namedtuple('Endpoint', ['name','host','zone']) 
#create a new datatype

region_to_endpoint={
    'us-east-2': Endpoint('US East (Ohio)', 's3-website.us-east-2.amazonaws.com','Z2O1EMRO9K5GLX'),
    'us-east-1': Endpoint('US East (N.Virginia)', 's3-website-us-east-1.amazonaws.com','Z3AQBSTGFYJSTF '),
    'ap-south-1': Endpoint('Asia Pacific (Mumbai)','s3-website.ap-south-1.amazonaws.com', 'Z11RGJOFQNVJUP'),
    'us-west-1': Endpoint('US West (N.California)','s3-website-us-west-1.amazonaws.com', 'Z2F56UZL2M1ACD'),
}

#helper functions
def known_region(region):
    """Returns true if this is a known region"""
    return region in region_to_endpoint

def get_endpoint(region):
    """Get the S3 webhosting endpoints for this region"""
    return region_to_endpoint[region]

# print(type(endpoint))
# ep1=endpoint('US East (Ohio)','s3-website.us-east-2.amazonaws.com','Z2O1EMRO9K5GLX')
# print(ep1.name)
# print(ep1.host)
