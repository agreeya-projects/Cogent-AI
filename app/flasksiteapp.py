import datetime
from openai import OpenAI
import os
import threading
#
from flask import Flask

os.environ["OPENAI_API_KEY"] = ""
# # from flask_sqlalchemy import SQLAlchemy
# # app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../Cogent-AI.db'
# # db = SQLAlchemy(app)
#
# # Set your OpenAI API key
# #openai.api_key = ""
# #-----------------
# # param= db.Client()
# from logging import *
#
# LOG_FORMAT="{lineno} *** {name} *** {asctime} *** {message}"
# basicConfig(filename='logfile.log',level=error,filemode='w',style='{',format=LOG_FORMAT)
#
# logger= getLogger()
# #
# # logger.debug("Debug logger")
# # logger.info("Info logger")
# # logger.warning("Warning  logger")
# # logger.error("Error logger")
# # logger.critical("Critical error logger")
#
# OpenAI.api_key = ""
# os.environ["OPENAI_API_KEY"] = ''
#
# # Initialize Flask app
app = Flask(__name__)
# from models import db, Client
# params = Client(clientid='1', clientname='Cogent',
#                        clientemail='jd@example.com', billinginformation='done',
#                        subscriptionid=0, modeltype='Eco',
#                        paymentstatus='not received', is_active=True,
#                        is_deleted=False)
#
# # Function to transcribe audio using OpenAI's Whisper API
#
def transcribe_audio(file_path):
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    OpenAI.api_key = openai_api_key
    client = OpenAI()
    print(datetime.datetime.now())

    try:
        audio_file= open(file_path, "rb")
        transcript = client.audio.transcriptions.create(
        model="whisper-1",
        language="en",
        file=audio_file
        )
        print(datetime.datetime.now())
        print(transcript)
    except Exception as e:
        # logger.error("Transcribe Audio whisper",e)
        print("Error:", e)

# Function to process all MP3 files in the "Recording" folder
def process_recordings():
    root_folder = "D:\Cogent_AI_Audio_Repo"
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                threading.Thread(target=transcribe_audio, args=(file_path,)).start()

# Route to trigger processing of recordings
@app.route('/')
def hello():
    """Renders a sample page."""
    # Run transcription for all MP3 files in separate threads
    threading.Thread(target=process_recordings).start()
    return "Transcription started for all recordings in the background."

if __name__ == '__main__':
    # Run Flask app
    app.run(threaded=True)  # Enable multithreading


from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Cogent/AI_Repo/Cogent-AI/app/'
# db = SQLAlchemy(app)

# Reflect the database tables
# Base = automap_base()
# Base.prepare(db.engine, reflect=True)

# Access the models dynamically
# with app.app_context():
#     Base = automap_base()
#     Base.prepare(db.engine, reflect=True)
#     Client = Base.classes.client

# Route to handle GET request for retrieving user data
# import app
# from db_connection import DbConnection
#
# db_instance = DbConnection()
# db_instance.connect_to_database()

# @app.route('/postclient', methods=['GET'])
# def add_client():
#     pass
    # with app.app_context():
    # params = Client(clientid='11211', clientname='Cogent381',
    # clientemail = 'jd1@example821.com', billinginformation = 'done731',
    # subscriptionid = 101010, modeltype = 'Eco123',
    # paymentstatus = '1not receive2411', is_active = False,
    # is_deleted = True)
    # db.session.add(params)
    # db.session.commit()
    # return "Success"

#Retreive all client details
#####Fetch for this connection#########

# from db_utils import DBRecord
# db_instance = DBRecord()

############----------End##############

# @app.route('/get_all_data', methods=['GET'])
# def get_record():
#     # with app.app_context():
#     table_name = request.args.get('table_name')
#     print("11111111TTTTT",table_name)
#     data = db_instance.get_all_record(table_name)
#     print(22222222222,data)
#     if data ==None:
#         data={"Error":"Invalid table/Data not available for this "+ table_name}
#     return data

#single client details

# @app.route('/get_record_by_id', methods=['GET'])
# def get_recordby_id():
#     table_name = request.args.get('table_name')
#     id = request.args.get('id')
#     data = db_instance.get_single_record(table_name,id)
#     print("BYYYYYYYYYYYYID>>", data)
#     if data == None:
#         data={"Error":"Invalid table/Data not available for this "+ table_name}
#     return data

# @app.route('/delete_record_by_id')
# def delete_recordby_id():
#     table_name = request.args.get('table_name')
#     itm_id = request.args.get('id')
#     data = db_instance.delete_single_record(table_name,itm_id)
#     if data == None:
#         data={"Error":"Invalid table/Data not available for this "+ table_name}
#     return {'data': data}

# @app.route('/get_record_by_column_name', methods=['GET'])
# def get_recordby_column_name():
#     table_name = request.args.get('table_name')
#     column_name = request.args.get('column_name')
#     column_value = request.args.get('column_value')
#     print("cccccccccccccccc",column_value)
#     # id = request.args.get('id')
#     data = db_instance.get_data_by_column_name(table_name,column_value)
#     print("BYYYYYYYYYYYYID>>column", data)
#     if data == None:
#         data={"Error":"Invalid table/Data not available for this "+ table_name}
#     return data
# if __name__ == '__main__':
#     app.run(debug=True,port=5361)
