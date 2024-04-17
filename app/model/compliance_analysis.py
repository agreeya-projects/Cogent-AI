from app.services.logger import Logger
import os
import json
from app.utilities.utility import GlobalUtility
from datetime import datetime
from db_layer.models import AudioTranscribeTracker,ScoreCardAnalysis,AudioTranscribe,ComplianceScore,JobStatus
from sqlalchemy.exc import IntegrityError
from app.configs.error_code_enum import *
from app import prompt_check_list
os.environ["OPENAI_API_KEY"] = prompt_check_list.open_ai_key
from flask_end_points_service import set_json_format
from openai import OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class ComplianceAnalysisCreation:

    def __init__(self):
        self.logger = Logger()
        self.global_utility = GlobalUtility()


    def compliance_analysis(self, trans_text,compliance_check_list):
        try:
            status = 'success'
            prompt = "{} {} {} @@@ {}.@@@".format(prompt_check_list.compliance_prompt, compliance_check_list, prompt_check_list.compliance_prompt_after_checklist ,trans_text)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                # model="gpt-4",
                messages=[
                    # {"role": "system", "content": prompt},
                    {"role": "user", "content": prompt}
                ],

                max_tokens=1500,
                n=1,
                presence_penalty=0.8,
                temperature=0.2,
                top_p=1.0,
                stop=None
                # stop=["\n"]
            )
            sentiment = response.choices[0].message.content
            results = json.loads(sentiment)
            data = {'OverallScore':results['OverallScore'],'Scorecard':results}
            return status, data
        except Exception as e:
            status = 'failure'
            error_array = []
            error_array.append(str(e))
            self.logger.error(f" Sentiment Error in method get_sentiment", str(e))
            return status, set_json_format(error_array, 500, False, str(e))


    def data_dump_into_compliance_database(self, server_name, database_name, client_id,transcribe_data):
        connection_string = self.global_utility.get_connection_string(server_name, database_name, client_id)
        if len(connection_string) > 0:
            session = self.global_utility.get_database_session(connection_string)
            try:
                # prompt_inject= self.get_prohibited_data_from_table(server_name, database_name, client_id)
                transcribe_audio_data=transcribe_data.get("TranscribeMergeText")
                transcribe_merged_string = '.'.join(transcribe_audio_data)
                clientid=transcribe_data.get("ClientId")
                current_file=transcribe_data.get("filename")
                created_compliance_date = datetime.utcnow()
                analysis_compliance_date = datetime.utcnow()
                modified_compliance_date = datetime.utcnow()
                file_entry_check = session.query(ScoreCardAnalysis).filter_by(AudioFileName=current_file).all()
                if len(file_entry_check) == 0:
                    compliance_check_list= self.get_data_from_compliance_score(server_name, database_name, client_id)
                    status, compliance_data = self.compliance_analysis(transcribe_merged_string,compliance_check_list[0])
                    dump_data_into_table = ScoreCardAnalysis(ClientId=clientid,
                                                             ScoreCardStatus=22,
                                                             AnalysisDateTime=analysis_compliance_date,
                                                             ScoreCard=str(compliance_data['Scorecard']),
                                                             ComplianceSummary='',
                                                             Created=created_compliance_date,
                                                             Modified=modified_compliance_date,
                                                             AudioFileName=current_file,
                                                             OverallScore=str(compliance_data['OverallScore']),
                                                             )
                    if status == 'success':
                        session.add(dump_data_into_table)
                        session.commit()
                        # result=set_json_format([], SUCCESS, True, f"Compliance Record successfully recorded for the file {current_file}")
                        result= {"status":SUCCESS, "message": f"Compliance Record successfully recorded for the file {current_file}"}
                        return result,SUCCESS
                    else:
                        return compliance_data,RESOURCE_NOT_FOUND
                else:
                    result={"status":SUCCESS,"message":f"Compliance Record already available for this {current_file}"}
                    return result,SUCCESS

            except IntegrityError as e:
                self.logger.error(f"Found error in data_dump_into_compliance_database or get_sentiment",str(e))
                error_array = []
                error_array.append(str(e))
                self.logger.error(f" Compliance Error in method compliance_analysis", str(e))
                return set_json_format(error_array, e.args[0].split(":")[1].split("-")[0].strip(), False, str(e)),RESOURCE_NOT_FOUND
            except Exception as e:
                self.logger.error(f"Found error in data_dump_into_compliance_database or compliance_analysis", str(e))
                error_array = []
                error_array.append(str(e))
                self.logger.error(f" Compliance Error in method compliance_analysis", str(e))
                return set_json_format(error_array, e.args[0].split(":")[1].split("-")[0].strip(), False, str(e))
            finally:
                session.close()
        else:
            result = {'status': INTERNAL_SERVER_ERROR, "message": "Unable to connect to the database"}
            return result, INTERNAL_SERVER_ERROR

    def get_transcribe_data_for_compliance(self, server_name, database_name, client_id,audio_file):
        self.logger.log_entry_into_sql_table(server_name, database_name, client_id, False)
        connection_string = self.global_utility.get_connection_string(server_name, database_name, client_id)
        if len(connection_string) > 0:
            session = self.global_utility.get_database_session(connection_string)
            try:
                audio_dictionary = {}
                transcribe_text = []
                check_audio_file_exits = session.query(AudioTranscribe).filter(
                    AudioTranscribe.AudioFileName == audio_file).all()
                if len(check_audio_file_exits) > 0:
                    audio_id_query = session.query(AudioTranscribe.Id).filter(
                        AudioTranscribe.AudioFileName == audio_file)
                    query_audio_id_results = audio_id_query.all()
                    check_chunk_exist = session.query(AudioTranscribeTracker.ChunkText).filter(
                        AudioTranscribeTracker.AudioId == query_audio_id_results[0][0])
                    # blank_emails = session.query(AudioTranscribeTracker).filter(AudioTranscribeTracker.ChunkText == '').all()
                    chunk_results_check = check_chunk_exist.all()
                    if len(query_audio_id_results) > 0 and chunk_results_check[0][0] !=None:
                        query = session.query(AudioTranscribeTracker.ClientId, AudioTranscribeTracker.AudioId,
                                              AudioTranscribeTracker.ChunkFilePath,
                                              AudioTranscribeTracker.ChunkSequence,
                                              AudioTranscribeTracker.ChunkText).filter(
                            AudioTranscribeTracker.AudioId == audio_id_query)
                        results = query.all()
                        for row in results:
                            print("row outpupt", row.ClientId)
                            transcribe_text.append(row.ChunkText)
                            audio_dictionary.update({"ClientId": row.ClientId, "TranscribeId": row.AudioId,
                                                     "ChunkSequence": row.ChunkSequence,
                                                     "TranscribeMergeText": transcribe_text,"filename":audio_file})
                    else:
                        self.logger.info(f":Transcribe Job Status is pending")
                        data= {"status":RESOURCE_NOT_FOUND,"message":f":ChunkText is not exist for {audio_file} in AudioTranscribeTracker Table"}
                        return data,RESOURCE_NOT_FOUND
                else:
                    self.logger.info(f":Record not found {audio_file}")
                    data= {"message":f":Record not found {audio_file} in AudioTranscribe Table"}
                    return data,RESOURCE_NOT_FOUND
                return self.data_dump_into_compliance_database(server_name, database_name, client_id, audio_dictionary)
            except Exception as e:
                # self.logger.error(f": Error {e}",e)
                error_array = []
                error_array.append(str(e))
                self.logger.error('Error in Method get_connection_string ', str(e))
                return set_json_format(error_array, INTERNAL_SERVER_ERROR, False, str(e))
                # result.close()
            finally:
                self.logger.log_entry_into_sql_table(server_name, database_name, client_id, True)
                session.close()
        else:
            result = {'status': INTERNAL_SERVER_ERROR, "message": "Unable to connect to the database"}
            return result,INTERNAL_SERVER_ERROR

    def get_data_from_compliance_score(self, server_name, database_name, client_id):
        self.logger.log_entry_into_sql_table(server_name, database_name, client_id, False)
        connection_string = self.global_utility.get_connection_string(server_name, database_name, client_id)
        if len(connection_string) > 0:
            session = self.global_utility.get_database_session(connection_string)
            try:
                compliance_score = session.query(ComplianceScore).all()
                compliance_data=""
                if len(compliance_score) > 0:
                    result = session.query(ComplianceScore.Compliance).filter_by(ClientID=client_id).all()
                    numbered_topics = [f"{i}) {result[0]}\n" for i, result in enumerate(result, start=1)]
                    for topic in numbered_topics:
                        compliance_data += topic
                    self.logger.info(f":Get Data from compliance Score successfully for ClientID {client_id}")
                    return compliance_data,SUCCESS
                else:
                    self.logger.info(f":Compliance data not available for ClientID{client_id}")
                    result = {'status': RESOURCE_NOT_FOUND, "message": "Compliance data not available !"}
                    return result,RESOURCE_NOT_FOUND
            except Exception as e:
                error_array = []
                error_array.append(str(e))
                self.logger.error('Error in Method get_data_from_compliance_score ', str(e))
                return set_json_format(error_array, INTERNAL_SERVER_ERROR, False, str(e))
            finally:
                self.logger.log_entry_into_sql_table(server_name, database_name, client_id, True)
                session.close()
        else:
            result = {'status': INTERNAL_SERVER_ERROR, "message": "Unable to connect to the database"}
            return result, INTERNAL_SERVER_ERROR