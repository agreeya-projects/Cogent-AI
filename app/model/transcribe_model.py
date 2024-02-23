import os
from app.utilities.utility import GlobalUtility
from app.controllers.controllers import Controller
class TranscribeModel: 
    global_utility =  GlobalUtility()
    controller = Controller()       
    def __init__(self):
        # self.model = model
        self.global_utility =  GlobalUtility()
        self.controller = Controller() 

    def build_transcribe_model(self,source_file_path,destination_path,subscription_model):
        try:
            print('source_file_path console :- ',source_file_path)
            print('destination_path console :- ',destination_path)
            file_collection = self.global_utility.get_all_files(source_file_path)
            # model details, subscription
            self.start_process_model(file_collection,source_file_path,destination_path,subscription_model)
            # create_folder_structure(file_collection,source_file_path,destination_path,subscription_model)
        except Exception as e:   
            print('Error while creating build_transcribe_model',e)
    
    def start_process_model(self,file_collection,source_file_path,destination_path,subscription_model):
        try:
            for file in file_collection:
                file_url = source_file_path+"/"+file;
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
                            chunks = self.global_utility.split_audio_chunk_files(audio_file_path,dir_folder_url)
                            chunks_files = chunks[0]
                            chunk_chunk_files_path = chunks[1]
                            txt_file = os.path.join(dir_folder_url, name_file)+'.txt'
                            for i in range(len(chunks_files)):
                                chunk_file = f"{dir_folder_url}/chunk_{i}.wav"
                                print(' Open Ai Chunk Audio File Path',chunk_file) 
                                # transcript = self.controller.build_chunk_files_transcribe_audio(self,chunks[0],chunks[1],subscription_model)
                                transcript = self.controller.build_transcribe_audio(chunk_file,subscription_model)
                                is_text_file_written = self.global_utility.wrire_txt_file(txt_file,transcript)
                        else:
                            txt_file = dir_folder_url+'.txt'
                            transcript = self.controller.build_transcribe_audio(self,chunk_file,chunks[1],subscription_model)
                            is_text_file_written =self.global_utility.wrire_txt_file(txt_file,transcript)
        except Exception as e:   
            print('Error while creating build_transcribe_model',e)

   