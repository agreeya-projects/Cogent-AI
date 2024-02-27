import os
from app.utilities.utility import GlobalUtility
from app.controllers.controllers import Controller
from app.services.logger import Logger
import threading

class StartTranscribe:   
    controller = Controller()       
    def __init__(self):      
        self.global_utility =  GlobalUtility.get_instance()
        self.controller = Controller() 
        self.logger = Logger.get_instance()
    
    # @classmethod
    # def get_instance(cls):
    #     if cls._instance is None:
    #         cls._instance = cls.__new__(cls)
    #     return cls._instance

    def start_transcribe_process(self,source_file_path,destination_path,subscription_model):
        try:
            print('source_file_path console :- ',source_file_path)
            print('destination_path console :- ',destination_path)
            file_collection = self.global_utility.get_all_files(source_file_path)          
            self.start_recording_transcribe_process(file_collection,source_file_path,destination_path,subscription_model)            
        except Exception as e:   
            print('Error while creating build_transcribe_model',e)
    
    def start_recording_transcribe_process(self,file_collection,source_file_path,destination_path,subscription_model):
        try:
            transcribe_files =[]
            for file in file_collection:
                file_url = source_file_path+"/"+file;
                file_name, extension = self.global_utility.get_file_extension(file)
                if extension == ".wav" or extension == ".mp3": 
                    name_file =file_url.split('/')[-1].split('.')[0]
                    dir_folder_url = os.path.join(destination_path, name_file)
                    print('Audio File name for folder creation : ',name_file) 
                # model details, subscription
                    is_folder_created =self.global_utility.create_folder_structure(file,dir_folder_url,destination_path)
                    if is_folder_created:
                        is_copied_files = self.global_utility.copy_file(file_url,dir_folder_url)
                        if is_copied_files:
                            audio_file_path = os.path.join(dir_folder_url, file)
                            file_size = os.path.getsize(audio_file_path)                        
                            file_size_mb = file_size / (1024 * 1024)                        
                            if file_size_mb > 5:
                                print('file size :- ',file_size)
                                self.start_process_recordings_large_file(audio_file_path,dir_folder_url,name_file,subscription_model,transcribe_files)  
                                # threading.Thread(target=self.process_recordings(audio_file_path,dir_folder_url,name_file)).start()                  
                                # chunks = self.global_utility.split_audio_chunk_files(audio_file_path,dir_folder_url)
                                # chunks_files = chunks[0]
                                # chunk_chunk_files_path = chunks[1]
                                # txt_file = os.path.join(dir_folder_url, name_file)+'.txt'
                                # for i in range(len(chunks_files)):
                                #     chunk_file = f"{dir_folder_url}/chunk_{i}.wav"
                                #     print(' Open Ai Chunk Audio File Path',chunk_file) 
                                #     # transcript = self.controller.build_chunk_files_transcribe_audio(self,chunks[0],chunks[1],subscription_model)
                                #     transcript = self.controller.build_transcribe_audio(chunk_file,subscription_model)
                                #     is_text_file_written = self.global_utility.wrire_txt_file(txt_file,transcript)
                            else:
                                self.start_process_recordings(audio_file_path,dir_folder_url,name_file,subscription_model,transcribe_files)
                                # txt_file = dir_folder_url+'.txt'
                                # transcript = self.controller.build_transcribe_audio(self,chunk_file,chunks[1],subscription_model)
                                # is_text_file_written =self.global_utility.wrire_txt_file(txt_file,transcript)
                        else:
                            self.logger.error('start_recording_transcribe_process',f"{file} is not copied  in the destination folder {dir_folder_url}")
                    else:
                        self.logger.error('start_recording_transcribe_process',f"Folder is not created for the file {file}")
                else:   
                      self.logger.error('start_recording_transcribe_process',f"{file} is not supported.")       
            print("All Transcribe files: ", transcribe_files)
        except Exception as e:   
            self.logger.error('start_recording_transcribe_process',f'Error while creating build_transcribe_model {e}')
    
    def start_process_recordings_large_file(self,audio_file_path,dir_folder_url,name_file,subscription_model,transcribe_files):
        try:
            chunks = self.global_utility.split_audio_chunk_files(audio_file_path,dir_folder_url)
            chunks_files = chunks[0]
            # chunk_chunk_files_path = chunks[1]
            txt_file = os.path.join(dir_folder_url, name_file)+'.txt'
            transcribe_files.append(txt_file)
            for i in range(len(chunks_files)):
                chunk_file = f"{dir_folder_url}/chunk_{i}.wav"
                print(' Open Ai Chunk Audio File Path',chunk_file)           
                transcript = self.controller.build_transcribe_audio(chunk_file,subscription_model)
                # threading.Thread(target= transcript, args=(chunk_file,)).start()
                is_text_file_written = self.global_utility.wrire_txt_file(txt_file,transcript)
        except Exception as e:   
            self.logger.error('start_process_recordings_large_file',e)
    
    def start_process_recordings(self,audio_file_path,dir_folder_url,name_file,subscription_model,transcribe_files):
        try:            
            txt_file = os.path.join(dir_folder_url, name_file)+'.txt'                     
            transcript = self.controller.build_transcribe_audio(audio_file_path,subscription_model)           
            transcribe_files.append(txt_file)
            is_text_file_written = self.global_utility.wrire_txt_file(txt_file,transcript)
        except Exception as e:   
            self.logger.error('start_process_recordings',e)


    # def process_recordings(self,audio_file_path,dir_folder_url,name_file):      
    #     chunks = self.global_utility.split_audio_chunk_files(audio_file_path,dir_folder_url)
    #     chunks_files = chunks[0]
    #     chunk_chunk_files_path = chunks[1]
    #     txt_file = os.path.join(dir_folder_url, name_file)+'.txt'
    #     for i in range(len(chunks_files)):
    #         chunk_file = f"{dir_folder_url}/chunk_{i}.wav"
    #         print(' Open Ai Chunk Audio File Path',chunk_file) 
    #         # transcript = self.controller.build_chunk_files_transcribe_audio(self,chunks[0],chunks[1],subscription_model)
    #         transcript = self.controller.build_transcribe_audio(chunk_file,subscription_model)
    #         threading.Thread(target= transcript, args=(chunk_file,)).start()
    #         is_text_file_written = self.global_utility.wrire_txt_file(txt_file,transcript)
      