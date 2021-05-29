#app for menu and time 
from flask import Flask,render_template,request,jsonify
from werkzeug import secure_filename
from config import *
import boto3
import os

s3 = boto3.resource('s3',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
client = boto3.client('s3',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
app=Flask(__name__)

@app.route("/")
def main():
	return render_template('home.html')
	
@app.route("/show_upload")
def show_upload():
	return render_template('upload.html')
	
@app.route("/show_delete")
def show_delete():
	song_list=fetch_song_list()
	return render_template('delete.html',song_list=song_list)
	
@app.route("/addsong", methods=['POST','GET'])
def addsong():
	if request.method == 'POST':
	  f = request.files['file']
	  f.save(secure_filename(f.filename))
	  response=s3.meta.client.upload_file(secure_filename(f.filename),'bucket-name',secure_filename(f.filename))
	  os.remove(secure_filename(f.filename))
	  return 'file uploaded successfully'

@app.route("/list_delete_song", methods=['POST','GET'])
def list_delete_song():
	songs = request.form.getlist("delete_song")
	for song in songs:
		client.delete_object(
			Bucket='bucket-name',
			Key=song
		)
	song_list=fetch_song_list()
	return render_template('delete.html',song_list=song_list)

def fetch_song_list():
	response = client.list_objects(Bucket='bucket-name')
	if 'Contents' in response:
		song_list=[]
		for obj in response['Contents']:
			if obj['Key'] not in ["audio.json","news.json"]:
				song_list.append(obj['Key'])
			else:
				continue
		return song_list
	else:
		return "No Audio Found"
	
if __name__ == "__main__":
	#app.run(debug=True)
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)