import os
from flask import Flask, request, jsonify, json
from alchemy_encoder import AlchemyEncoder
from db_layer.models import Client, Configurations, Logs, FileTypesInfo, Subscriptions, AudioTranscribeTracker, \
    AudioTranscribe, ClientMaster, AuthTokenManagement
app = Flask(__name__)

from database_query_utils import *
from database_query_utils import DBRecord
from flack_service import FlaskDBService

db_instance = DBRecord()
flask_service = FlaskDBService()
server_name = 'FLM-VM-COGAIDEV'
database_name = 'AudioTrans'


@app.route('/get_all_data', methods=['GET'])
def get_record():
    table_name = request.args.get('table_name')
    data = db_instance.get_all_record(table_name)
    if data == None:
        data = {"Error": "Invalid table/Data not available for this " + table_name}
    return data


@app.route('/get_record_by_id', methods=['GET'])
def get_recordby_id():
    table_name = request.args.get('table_name')
    id = request.args.get('id')
    data = db_instance.get_record_by_id(table_name, id)
    if data == None:
        data = {"Error": "Invalid table/Data not available for this " + table_name}
    return data


@app.route('/get_record_by_column_name', methods=['GET'])
def get_recordby_column_name():
    table_name = request.args.get('table_name')
    column_name = request.args.get('column_name')
    column_value = request.args.get('column_value')

    data = db_instance.get_data_by_column_name(table_name, column_name, column_value)

    if data == None:
        data = {"Error": "Invalid table/Data not available for this " + table_name}
    return data


@app.route('/update_record_by_column', methods=['GET'])
def get_update_by_column_name():
    table_name = request.args.get('table_name')
    column_to_update = request.args.get('column_to_update')
    new_value = request.args.get('new_value')
    condition_column = request.args.get('condition_column')
    condition_value = request.args.get('condition_value')

    data = db_instance.update_record_by_column(table_name, column_to_update, new_value, condition_column,
                                               condition_value)

    if data == None:
        data = {"Error": "Invalid table/Data not available for this " + table_name}
    return data


@app.route('/delete_record_by_id')
def delete_recordby_id():
    table_name = request.args.get('table_name')
    itm_id = request.args.get('id')
    data = db_instance.delete_record_by_id(table_name, itm_id)
    if data == None:
        data = {"Error": "Invalid table/Data not available for this " + table_name}
    return {'data': data}

@app.route('/get_client_master_configurations', methods=['GET'])
def get_client_master_configurations():
    try:
        client_id = int(request.args.get('clientid'))
        results = session.query(ClientMaster).filter(Client.ClientId == client_id).all()
        if len(results) > 0:
            audio_transcribe_array = []
            for result in results:
                audio_transcribe_array.append(result.toDict())
            return flask_service.get_json_format(audio_transcribe_array)
        elif len(results) == 0:
            return flask_service.get_json_format([])
    except Exception as e:
        return flask_service.get_json_format([], False, e)

@app.route('/get_client_configurations', methods=['GET'])
def get_client_configurations():
    try:
        client_id = int(request.args.get('clientid'))
        results = session.query(Client).filter(
                (Client.ClientId == client_id) & (
                    Client.IsActive)).all()
        if len(results) > 0:
            result_array = []
            for result in results:
                result_array.append(result.toDict())
            return flask_service.get_json_format(result_array)
        elif len(results) == 0:
            return flask_service.get_json_format([])
    except Exception as e:
        return flask_service.get_json_format([], False, e)

@app.route('/get_audio_transcribe_data', methods=['GET'])
def get_audio_transcribe_data():
    try:
        client_id = int(request.args.get('clientid'))
        # data = database_service.get_audio_transcribe_table_data(server_name, database_name, client_id)
        audio_transcribe = session.query(AudioTranscribe).filter(
            (AudioTranscribe.ClientId == client_id) & (AudioTranscribe.JobStatus != 'Completed')).all()
        if len(audio_transcribe) > 0:
            audio_transcribe_array = []
            for result in audio_transcribe:
                audio_transcribe_array.append(result.toDict())
            return flask_service.get_json_format(audio_transcribe_array)
        elif len(audio_transcribe) == 0:
            return flask_service.get_json_format([])
        # data_json = json.dumps(data, cls=AlchemyEncoder)
    except Exception as e:
        return flask_service.get_json_format([], False, e)


@app.route('/get_audio_transcribe_tracker_data', methods=['GET'])
def get_audio_transcribe_tracker_data():
    try:
        client_id = int(request.args.get('clientid'))
        audio_id = int(request.args.get('audioid'))
        current_user = os.getlogin()
        print('Current login user:', current_user)
        audio_transcribe = session.query(AudioTranscribeTracker).filter(
            (AudioTranscribeTracker.ClientId == client_id) & (AudioTranscribeTracker.AudioId == audio_id) & (AudioTranscribeTracker.ChunkStatus != 'Completed')).all()
        if len(audio_transcribe) > 0:
            audio_transcribe_array = []
            for result in audio_transcribe:
                audio_transcribe_array.append(result.toDict())
            return flask_service.get_json_format(audio_transcribe_array)
        elif len(audio_transcribe) == 0:
            return flask_service.get_json_format([])
        # data_json = json.dumps(data, cls=AlchemyEncoder)
    except Exception as e:
        return flask_service.get_json_format([], False, e)

@app.route('/add_update_transcribe', methods=['GET'])
def add_update_transcribe():
    recored_id = int(request.args.get('id'))
    updatevalues = request.args.get('updatevalues')
    update_status = flask_service.update_audio_transcribe_table(server_name,database_name,recored_id,updatevalues)
    return update_status

@app.route('/add_update_transcribe_tracker', methods=['GET'])
def add_update_transcribe_tracker():
    recored_id = int(request.args.get('id'))
    updatevalues = request.args.get('updatevalues')
    update_status = flask_service.update_audio_transcribe_tracker_table(server_name,database_name,recored_id,updatevalues)
    return update_status



if __name__ == '__main__':
    app.run(debug=True)
