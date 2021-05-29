import boto3,json,re
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,date,time

aws_access_key_id = "XXX"
aws_secret_access_key = "UUU"
s3=boto3.resource('s3',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
client=boto3.client('s3',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
sched = BlockingScheduler()

response=client.list_objects(Bucket = "bucket name")#change the bucket name 

today=date.today()
todays_date = today.day
title_text=""
data_url=""

@sched.scheduled_job('interval', hour='00' , minutes='01')
#@sched.scheduled_job('interval', minutes=15)
def timed_job():		
	for record in response['Contents']:
		#datr_string = str(record['LastModified'])
		#print(record['Key'],re.split('\s',datr_string))
		if record['Key'].startswith(str(todays_date)):
			title_text=record['Key']
			data_url="https://s3-eu-west-1.amazonaws.com/bucket-name/"+record['Key']
	data=[

		{
			"uid": "udi",
			"updateDate": str(today)+"T00:00:00.0Z",
			"titleText": title_text,
			"mainText": "",
			"streamUrl":data_url,
			"redirectionUrl": "http://pohostaging.club/bucket-name/"
		}

	]
	with open("audio.json",'w+') as f:
		json.dump(data,f)

	resp_s3 = s3.meta.client.upload_file('audio.json', 'bucket', 'audio.json')
	print("Ran on "+str(today)+". Uploaded file is "+str(title_text))

sched.start()
	
