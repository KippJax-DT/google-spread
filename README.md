I use this lambda function template and code to deposit an item from our s3 buckets to our Google Drive and to a google sheet to be analyzed later for meetings. 

environment variables:  
  1. credentials:  name of your secret.json file for your service account to deposit data.
        API for google sheet must be enabled in the Google Cloud platform
  2. bucket:    Name of bucket where your csv or file is located in your aws account that you want to grab. 
  3. file_path: name of file in s3 bucket
  4. Google_file: name of file/sheet in google account you want to deposit into. This file must already exist and the service account must have editor access to this file [example spreadsheets being 'gift ideas' or 'budget sheet' ]
  5. assessment_titles: same as google file, this is just used for another file
  6. sm_file: name of file in s3 bucket

Again, this is a template and everything can be changed naming wise and you should be able to create your own ENV file to be able to import those variables. 

Thank you, everyone be safe!
