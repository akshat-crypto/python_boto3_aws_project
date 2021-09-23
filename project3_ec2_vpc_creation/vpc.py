from urllib3 import Retry
import boto3
import botostubs


# VPC is a part of ec2 service in documentation, we need to use the ec2 client to use the vpc services here



class VPC:
    """Class for using the vpc services"""
    def __init__(self,client):      #creating a client session for vpc here
        """Creating the ec2 client session here"""
        self._client=client         #private object _client of class VPC
        
    
    def create_vpc(self):
        """Creating the VPC here"""
        print("Creating new vpc...")
        cidr_range=input("Enter CIDR range: ")
        return self._client.create_vpc(
            CidrBlock=cidr_range
            # CidrBlock='10.0.0.0/16',
        )
    
    # def add_name_tags(self, *, resource_id, resource_name): #used the keyword only arguments here
    def add_name_tag(self,  resource_id, resource_name):
        print("Adding resources name here")
        return self._client.create_tags(
            Resources=[resource_id],    #provides a list because we can make changes in multiple resources
            Tags=[
                {
                    'Key': 'Name',
                    'Value': resource_name,
                }
                #we can provide here the two different dictionary also
            ]
        )
    
    def create_internet_gateway(self):
        print("Creating Internet Gateway...")
        return self._client.create_internet_gateway()   #it will create the internet gateway only
    
    def attach_igw_to_vpc(self,vpc_id,igw_id):
        print("Attaching Internet Gateway...")
        #can use menu to first retrieve the values of default vpcs and internet gateways
        return self._client.attach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id,
        )
    
    def create_subnet(self,vpc_id,cidr_block):
        print("Creating subnet")
        return self._client.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr_block,
        )
    
    def create_public_route_table(self,vpc_id):
        print('Creating public Route Table for VPC'+ vpc_id)
        return self._client.create_route_table(VpcId=vpc_id)
    
    def create_igw_route_to_public_route_table(self,rtb_id,igw_id):
        print('Adding Route for igw')
        return self._client.create_route(
            RouteTableId=rtb_id,
            GatewayId=igw_id,
            DestinationCidrBlock='0.0.0.0/0'
        )
    
    def associate_subnet_with_route_table(self,subnet_id, rtb_id):
        print('Assosciating Routes')
        return self._client.associate_route_table(
            SubnetId=subnet_id,
            RouteTableId=rtb_id,
        )
        
    def allow_auto_assign_ip_addresses_for_subnet(self,subnet_id):
        return self._client.modify_subnet_attribute(
            SubnetId=subnet_id,
            MapPublicIpOnLaunch={'Value': True}
        )
