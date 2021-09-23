
from vpc import VPC
from ec2 import EC2
from client_locator import EC2Client


def main():
    #create a vpc
    ec2_client=EC2Client().get_client()
    vpc=VPC(ec2_client)     #vpc resources are subpart of ec2 here
    
    vpc_response= vpc.create_vpc()  #calls the function and stores its response
    
    print("Vpc Created: " + str(vpc_response))  #converts the dict type into string
    
    #adds the name to the vpc
    print()
    vpc_name=input("Enter VPC new name: ")
    vpc_id=vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id,vpc_name)
    
    print("Added name tag: "+vpc_name + "to: " + vpc_id)
    
    
    #create an igw
    igw_response=vpc.create_internet_gateway()
    
    igw_id=igw_response['InternetGateway']['InternetGatewayId']
    
    vpc.attach_igw_to_vpc(vpc_id=vpc_id,igw_id=igw_id)
    
    
    #creates a public subnet -we need to attach specific rules in the routing table
    public_subnet_response = vpc.create_subnet(vpc_id, '10.0.1.0/24')   #passing the cidr range in here
    public_subnet_id= public_subnet_response['Subnet']['SubnetId']
    
    print('Subnet created for VPC ' + vpc_id + ':' + str(public_subnet_response))
     
    # Add name tag to Public Subnet
    vpc.add_name_tag(public_subnet_id, 'Test-Public-Subnet') 
    
    # Create a public route table
    public_route_table_response = vpc.create_public_route_table(vpc_id)
    
    rtb_id = public_route_table_response['RouteTable']['RouteTableId']
    
    # Adding the IGW to public route table
    vpc.create_igw_route_to_public_route_table(rtb_id, igw_id)

    # Associate Public Subnet with Route Table
    vpc.associate_subnet_with_route_table(public_subnet_id, rtb_id)

     # Allow auto-assign public ip addresses for subnet
    vpc.allow_auto_assign_ip_addresses_for_subnet(public_subnet_id)

    # Create a Private Subnet
    private_subnet_response = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']

    print('Created private subnet ' + private_subnet_id + ' for VPC ' + vpc_id)

    # Add name tag to private subnet
    vpc.add_name_tag(private_subnet_id, 'Test-Private-Subnet')
    
    
    
    # * EC2 resources
    ec2 = EC2(ec2_client)

    # Create a key pair
    # key_pair_name = 'Boto3-KeyPair'
    key_pair_name=input("Enter Key Name: ")
    key_pair_response = ec2.create_key_pair(key_pair_name)
    
    print('Created Key Pair with name ' + key_pair_name + ':' + str(key_pair_response))

    # Create a Security Group
    public_security_group_name = 'Boto3-Public-SG'
    public_security_group_description = 'Public Security Group for Public Subnet Internet Access'
    public_security_group_response = ec2.create_security_group(public_security_group_name, public_security_group_description, vpc_id)
    
    public_security_group_id = public_security_group_response['GroupId']
    
    # Add Public Access to Security Group
    ec2.add_inbound_rule_to_sg(public_security_group_id)
    
    print('Added public access rule to Security Group ' + public_security_group_name)

    user_data = """#!/bin/bash
                yum update -y
                yum install httpd -y
                systemctl start httpd
                echo "<html><body><h1>Boto3 using Python! Scripts Example</h1></body></html>" > /var/www/html/index.html"""
                
    
    ami_id = 'ami-087c17d1fe0178315'
    
    # Launch a public EC2 Instance
    ec2.launch_ec2_instance(ami_id, key_pair_name, 1, 1, public_security_group_id, public_subnet_id, user_data)

    print('Launching Public EC2 Instance using AMI ' + ami_id)
    

def describe_instances():
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)

    ec2_response = ec2.describe_ec2_instances()

    print(str(ec2_response))


def modify_instance():
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)

    ec2.modify_ec2_instance('i-01560b6cd12a884a1')


def stop_instance():
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)

    ec2.stop_instance('i-049f27f4be7441270')


def start_instance():
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)

    ec2.start_instance('i-049f27f4be7441270')


def terminate_instance():
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)

    ec2.terminate_instance('i-049f27f4be7441270')


if __name__ == '__main__':
    main()
    # describe_instances()
    # modify_instance()
    # stop_instance()
    # start_instance()
    # terminate_instance()