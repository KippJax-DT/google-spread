# from google.cloud import storage
import boto3
import pandas as pd
import logging
from io import StringIO
import os
# import necessary packages
import gspread
from oauth2client.service_account import ServiceAccountCredentials
    


def lambda_handler(event,context):
    """  
    First we would like to read the file that is in our s3 bucket.
    We use boto3.resource to be able to do this. Once that has occured, we are able to download the file to our docker container
    After the file is downloaded, it is available to the download path that we have it set to This is important
    Once refrencing it, we are forced to use the google Auth client. Once this is signed in, we can have it be that it does not need to be authorized anymore.   
    """

    #   This is to read the file from our s3 bucket in AWS. This is okay and does not need to be edited
    s3 = boto3.client('s3')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # bucket_name = os.environ.get('bucket_name')
    bucket_name = os.environ.get('bucket_name')


    # cloud_file_name = os.environ.get('file_path')
    cloud_file_name =  os.environ.get('file_path')
    sm_file = os.environ.get('sm_file')
    

    logger.info(f"file: {cloud_file_name}")
    logger.info(f"Reading Bucket: {bucket_name}")
    logger.info(f"file: {sm_file}")

    assess_object = s3.get_object(Bucket = bucket_name, Key = cloud_file_name)
    assess_body = assess_object['Body'].read().decode('utf-8')
    
    standards_object = s3.get_object(Bucket= bucket_name, Key = sm_file)
    standards_body = standards_object['Body'].read().decode('utf-8')
    

    # Create Stringio reading object

    assess_io = StringIO(assess_body)
    sm_io = StringIO(standards_body)

    assessments_df = pd.read_csv(assess_io)
    sm_df = pd.read_csv(sm_io)
    
    logger.info(f"Data loaded from S3. First 5 rows:\n{assessments_df.head()}")
    
    logger.info(f"There are {assessments_df.shape[0]} different types of assessments and code scopes.")
    assessments_df.to_csv(f"/tmp/assessments.csv")
    sm_df.to_csv("/tmp/standards.csv")
    
    #  --------------------------

    #  Next we want to use gspread to be albe to deposit the csv as a google sheet that is in our drive. 

    """ These scope items are required to use. Read Documentation here:  /n
        https://docs.gspread.org/en/latest/
    
    """

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    #  After enabling google sheets api and the google drive api, we are able to deposit the items and csvs that we need.
    cred_file_name = os.environ.get('credentials')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file_name,scope)
    client = gspread.authorize(credentials)
    
    
    Assessments_file = os.environ.get("google_file")    
    spreadsheet = client.open(Assessments_file)

    with open('/tmp/assessments.csv', 'r') as file_obj:
        content = file_obj.read()
        client.import_csv(spreadsheet.id, data=content)
    
    logger.info(f"output: {spreadsheet}")
    
    print(f"Google file {Assessments_file} has been updated.")
    
    standards_file = os.environ.get("assessment_titles")
    
    spreadsheet = client.open(standards_file)
    with open('/tmp/standards.csv', 'r') as file_obj:
        content = file_obj.read()
        client.import_csv(spreadsheet.id, data=content)
        
    logger.info(f"Output : {spreadsheet}")

    
    