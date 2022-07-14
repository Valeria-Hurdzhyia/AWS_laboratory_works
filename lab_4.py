import boto3
import os
import pandas
import botocore
from botocore.exceptions import ClientError

def create_key_pair(key_name, region_name):
    ec2_client = boto3.client("ec2", region_name)
    try:
        key_pair = ec2_client.create_key_pair(KeyName=key_name)
        private_key = key_pair["KeyMaterial"] 
        print("The key pair", key_name, "successfully created!")
            
    except Exception as e:
        if type(e) == botocore.exceptions.ClientError:
            print("Client Error:", end=' ')
            if e.response['Error']['Code'] == "InvalidKeyPair.Duplicate":
                print("The key pair", key_name, "already exist!")
            else:
                print("Error:", e)
        elif type(e) == botocore.exceptions.EndpointConnectionError:
            print("Endpoint Connection Error:", "Check your region name!")
        else:
            print("Error:", e)
    
#create_key_pair("testik", "eu-west-1")



def create_instance(region_name, InstanceType, KeyName):
    ec2_client = boto3.client("ec2", region_name)
    try:
        instances = ec2_client.run_instances(
        ImageId="ami-0a8a24772b8f01294",
        MinCount=1,
        MaxCount=1,
        InstanceType=InstanceType,
        KeyName=KeyName
        )
        print("Instance successfully created!")
        print("Instance ID:", instances["Instances"][0]["InstanceId"])
    except Exception as e:
        if type(e) == botocore.exceptions.ClientError:
            print("Client Error:", end=' ')
            if e.response['Error']['Code'] == "InvalidKeyPair.NotFound":
                print("key not found")
            elif e.response['Error']['Code'] == "InvalidAMIID.Malformed":
                print("Wrong ImageID")
            elif e.response['Error']['Code'] == "InvalidParameterValue":
                print("Wrong instance type")
            else:
                print("Error:", e)
        elif type(e) == botocore.exceptions.EndpointConnectionError:
            print("EndpointConnectionError:", "Check your region name!")
        else:
            print("Error:", e)
#create_instance("us-west-1", "t2.micro", "testik")



def get_public_ip(instance_id, region_name):
    ec2_client = boto3.client("ec2", region_name)
    try:
        reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")
        for reservation in reservations:
            for instance in reservation['Instances']:
                print("Public Ip Address:", instance.get("PublicIpAddress"))
                
    except Exception as e:
        if type(e) == botocore.exceptions.ClientError:
            print("Client Error:", end=' ')
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                print("Invalid instance ID!")
            elif e.response['Error']['Code'] == "InvalidInstanceID.NotFound":
                print("Instance ID does not exist!")
            else:
                print("Error:", e)
        elif type(e) == botocore.exceptions.EndpointConnectionError:
            print("EndpointConnectionError:", "Check your region name!")
        else:
            print("Error:", e)
    
#get_public_ip("i-06864239172e16c52", "us-west-2")



def get_running_instances(region_name):
    ec2_client = boto3.client("ec2", region_name)
    try:
        reservations = ec2_client.describe_instances(Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"],
            },
            {
                "Name": "instance-type",
                "Values": ["t2.micro"]
            }
        ]).get("Reservations")

        count=0
        for reservation in reservations:
            count+=1
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                public_ip = instance["PublicIpAddress"]
                private_ip = instance["PrivateIpAddress"]
                print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")
        print("Count of running instances:", count)
                
    except Exception as e:
        if type(e) == botocore.exceptions.EndpointConnectionError:
            print("EndpointConnectionError:", "Check your region name!")
        else:
            print("Error:", e)
            
#get_running_instances("us-west-1")



def stop_instance(instance_id, region_name):
    ec2_client = boto3.client("ec2", region_name)
    try:
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        print("Instance was successfully stoped!")
        print(response)
        
    except Exception as e:
        if type(e) == botocore.exceptions.ClientError:
            print("Client Error:", end=' ')
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                print("Invalid instance ID!")
            elif e.response['Error']['Code'] == "InvalidInstanceID.NotFound":
                print("Instance ID does not exist!")
            else:
                print("Error:", e)
        elif type(e) == botocore.exceptions.EndpointConnectionError:
            print("EndpointConnectionError:", "Check your region name!")
        else:
            print("Error:", e)
    
#stop_instance("i-0f982df6b1f82b8b2", "us-west-1")




def terminate_instance(instance_id, region_name):
    ec2_client = boto3.client("ec2", region_name)
    try:
        response = ec2_client.terminate_instances(InstanceIds=[instance_id])
        print("Instance was successfully terminated!")
        print(response)
    except Exception as e:
        if type(e) == botocore.exceptions.ClientError:
            print("Client Error:", end=' ')
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                print("Invalid instance ID!")
            elif e.response['Error']['Code'] == "InvalidInstanceID.NotFound":
                print("Instance ID does not exist!")
            elif e.response['Error']['Code'] == "OperationNotPermitted":
                print("Operation Not Permitted!")
            else:
                print("Error:", e)
        elif type(e) == botocore.exceptions.EndpointConnectionError:
            print("EndpointConnectionError:", "Check your region name!")
        else:
            print("Error:", e)
    
#terminate_instance("i-09ed0315a492e9cf1", "us-west-1")






def create_bucket(bucket_name, region):
    s3_client = boto3.client('s3', region_name=region)
    try:
        location = {'LocationConstraint': region}
        response = s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print("Bucket was successfully created!")
        print(response)
    except Exception as e:
        if type(e) == botocore.exceptions.ClientError:
            print("Client Error:", end=' ')
            if e.response['Error']['Code'] == "InvalidBucketName":
                print("Invalid Bucket Name!")
            else:
                print("Error:", e)
        elif type(e) == botocore.exceptions.EndpointConnectionError:
            print("EndpointConnectionError:", "Check your region name!")
        else:
            if e.response['Error']['Code'] == "BucketAlreadyOwnedByYou":
                print("You already have bucket with this name!")
            elif e.response['Error']['Code'] == "BucketAlreadyExists":
                print("Bucket with this name already exist!")
            else:
                print("Error:", e)
                return e
#create_bucket("lab-pti", "us-west-1")



def show_existing_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    print("Existing buckets:")
    for bucket in response['Buckets']:
        print(f' {bucket["Name"]}')
#show_existing_buckets()


def upload(file_name, bucket_name, s3_obj_name):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(Filename=file_name, Bucket=bucket_name, Key=s3_obj_name)
        print("file was successfully uploaded!")
        print(response)
   
    except FileNotFoundError:
        print("File not found!")
        
    except boto3.exceptions.S3UploadFailedError as e:
        print("No such bucket or access to this bucket denied")

    except Exception as e:
        print("Error:", e)
            
#upload("data.csv", "lab--pti", "data.csv")



def show_context_of_bucket(bucket_name, key_name):
    s3_client = boto3.client('s3')
    try:
        obj = s3_client.get_object(Bucket = bucket_name, Key = key_name)
        # Read data from the S3 object
        data = pandas.read_csv(obj['Body'])
        # Print the data frame
        print('Printing the data frame...')
        print(data.head())

    except ClientError as e:
        print("Client Error:", end=' ')
        if e.response['Error']['Code'] == "NoSuchBucket":
            print("No Such Bucket")
        elif e.response['Error']['Code'] == "NoSuchKey":
            print("No Such File")
        elif e.response['Error']['Code'] == "AccessDenied":
            print("Access Denied")
        else:
            print("Error:", e)

#show_context_of_bucket("lab-pti", "data.csv")


def destroy_bucket(bucket_name):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.delete_bucket(Bucket=bucket_name)
        print("Bucket successfully deleted!")
        print(response)
        
    except ClientError as e:
        print("Client Error:", end=' ')
        if e.response['Error']['Code'] == "NoSuchBucket":
            print("No Such Bucket")
        elif e.response['Error']['Code'] == "BucketNotEmpty":
            print("Bucket is not Empty")
        elif e.response['Error']['Code'] == "AccessDenied":
            print("Access Denied")
        else:
            print("Error:", e)
#destroy_bucket("lab-pti")


if __name__ == "__main__":
    while True:
        print("Amazon Web Service")
        print("1) Enter to EC2")
        print("2) Enter to S3")
        print("3) Exit")
        
        print("Your choice:", end=' ')
        choice = int(input())
        
        if choice == 1:
            
            while True:
                print("1) Create Key Pair")
                print("2) Create Instance")
                print("3) Get Public IP")
                print("4) Get Running Instances")
                print("5) Stop Instance")
                print("6) Terminate Instance")
                print("7) Exit")

                print("Your choice:", end=' ')
                choice = int(input())

                if choice == 1:
                    print("Enter key name:", end=' ')
                    key_name = input() 
                    print("Enter region:", end=' ')
                    region_name = input()
                    create_key_pair(key_name, region_name)
                elif choice == 2:
                    print("Enter region:", end=' ')
                    region_name = input()
                    print("Enter instance type:", end=' ')
                    InstanceType = input() 
                    print("Enter key pair:", end=' ')
                    KeyName = input() 
                    create_instance(region_name, InstanceType, KeyName)
                elif choice == 3:
                    print("Enter instance ID:", end=' ')
                    instance_id = input()
                    print("Enter region:", end=' ')
                    region_name = input() 
                    get_public_ip(instance_id, region_name)
                elif choice == 4:
                    print("Enter region:", end=' ')
                    region_name = input() 
                    get_running_instances(region_name)
                elif choice == 5:
                    print("Enter instance ID:", end=' ')
                    instance_id = input()
                    print("Enter region:", end=' ')
                    region_name = input() 
                    stop_instance(instance_id, region_name)
                elif choice == 6:
                    print("Enter instance ID:", end=' ')
                    instance_id = input()
                    print("Enter region:", end=' ')
                    region_name = input() 
                    terminate_instance(instance_id, region_name)
                elif choice == 7:
                    print("bye")
                    break
                else:
                    print("Try again")
                
            
        elif choice == 2:
            while True:
                print("1) Create Bucket")
                print("2) Show Existing Buckets")
                print("3) Upload File")
                print("4) Show Context Of Bucket")
                print("5) destroy_bucket")
                print("6) Exit")

                print("Your choice:", end=' ')
                choice = int(input())

                if choice == 1:
                    print("Enter Bucket name:", end=' ')
                    bucket_name = input()
                    print("Enter region:", end=' ')
                    region = input() 
                    create_bucket(bucket_name, region)
                elif choice == 2:
                    show_existing_buckets()
                elif choice == 3:
                    print("Enter File name:", end=' ')
                    file_name = input()
                    print("Enter Bucket name:", end=' ')
                    bucket_name = input()
                    print("Enter Object name:", end=' ')
                    s3_obj_name = input()
                    upload(file_name, bucket_name, s3_obj_name)
                elif choice == 4:
                    print("Enter Bucket name:", end=' ')
                    bucket_name = input()
                    print("Enter Key name:", end=' ')
                    key_name = input()
                    show_context_of_bucket(bucket_name, key_name)
                elif choice == 5:
                    print("Enter Bucket name:", end=' ')
                    bucket_name = input()
                    destroy_bucket(bucket_name)
                elif choice == 6:
                    print("bye")
                    break
                else:
                    pritn("Try again")
        elif choice == 3:
            print("Good Bye!")
            break;
        else:
            print("Try again")
