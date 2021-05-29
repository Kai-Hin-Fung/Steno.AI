import os
from flask import Flask,request
from flask_cors import CORS
from google.cloud import storage
from google.oauth2 import service_account
from pymongo import MongoClient
from bson.objectid import ObjectId
#from config import GCS_BLOB_NAME, PATH_TO_GCP_JSON
from key_summ import key_summar
from transcriber import transcribe_audio
import json

abs_path=os.getcwd()
app = Flask(__name__)
CORS(app)
#key_name = PATH_TO_GCP_JSON

client = MongoClient('mongodb://localhost:27017')
db = client.transcriptionApp

#do all of the recording and transcriptions
@app.route('/recorded-audio', methods = ['POST'])

def audio():
    filename = request.headers['filename']
    keyword = request.headers['speechContext']
    fn=filename+'.wav'
    audio_path= os.path.join('audio-files',fn)
    with open(audio_path, "wb") as f:
        data = request.get_data()
        f.write(data)
    transcript = transcribe_audio(audio_path)
    with open (audio_path, 'w') as f2:
        f2.write(transcript)
    with open (audio_path, 'r') as tr:
        summary = key_summar (tr, keyword)
    #summary = key_summar(transcript, keyword)
    
    # Query to db

    insert_transcript_into_db(filename,transcript,summary)
    delete_Blob(fn)

    return ''

# Get All transcripts

@app.route('/transcript', methods = ['GET'])

def get_transcripts():

    transcription = db.transcriptions
    result = list(transcription.find({}))
    return json.dumps(result, default=str)

# Delete a single transcript

@app.route('/transcript-delete/<id>',methods = ['DELETE'])

def delete_transcript(id):

    id = ObjectId(id)
    transcription = db.transcriptions
    transcription.delete_one({"_id" : id})

    return 'Deleted Successfully'

# Route for uploading a audio or text file and return the transcript + summary

@app.route('/upload-file',methods = ['POST'])

def upload_audio():
    keyword = request.headers['speechContext']
    keywords = keyword.split(', ')
    filename = request.headers['filename']
    type = request.headers['type']
    type = type.split('/')
    type = type[1]
    # if text file
    file_path = os.path.join('audio-files',filename)
    if(type == 'plain'):
        data = request.get_data()
        with open(file_path, "wb") as f:
            f.write(data)
        
        with open(file_path,"r") as file:
            multipart_string = file.read()
            temp = multipart_string.split('Content-Type: text/plain')
            temp = temp[1]
            temp = temp.split('------')
            temp = temp[0]
            temp = temp.strip()
            with open(file_path,"w") as t:
                t.write(temp)
        summary = ""
        with open(file_path,"r") as text_file:
            transcript = text_file.read()
        for key in keywords:
            with open (file_path, 'r') as tr:
                summary += key_summar (tr, key)
        
        if len(filename.split('.'))>1:
            filename=filename.split('.')[0]
        insert_transcript_into_db(filename,transcript,summary)
        
    # else its an audio file
    else:
        data = request.get_data()
        with open(file_path, "wb") as f:
            f.write(data)
        transcript = transcribe_audio(file_path)
        with open (file_path, 'w') as f2:
            f2.write(transcript)
        summary = ""
        for key in keywords:
            with open (file_path, 'r') as tr:
                summary += key_summar (tr, key)
        if len(filename.split('.'))>1:
            filename=filename.split('.')[0]
        insert_transcript_into_db(filename,transcript,summary)

    return ''

# function to delete the audio blob from the cloud and from the local file system

def delete_Blob(audio_blob_name):
    os.remove(os.path.join(abs_path,'audio-files',audio_blob_name))

def insert_transcript_into_db(filename,transcript,summary):
    transcription = db.transcriptions
    transcription_object = {
        'transcription-name' : filename,
        'transcription-data' : transcript,
        'summary' : summary,  
    }
    insert_result = transcription.insert_one(transcription_object)

    return ''

if __name__ == '__main__':
    app.run(threaded=True)


