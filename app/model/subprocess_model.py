import whisper 
import openai
from pydub import AudioSegment
import subprocess
import shutil
import os
from datetime import datetime
from app.utilities.utility import GlobalUtility

class SubProcessModel:  
    _instance = None
    _logs = ""

    def __init__(self):       
        self.global_utility =  GlobalUtility()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def transcribe_by_subprocess(self,chunks_files,chunk_directory,chunks,filename):   
        for i in range(len(chunks_files)):   
                chunk_file = f"{chunk_directory}/chunk_{i}.wav"          
                print("subprocess Start...", str(datetime.now()))       
                subprocess.run(["whisper", chunk_file, "--model", "base","--language", "en", "--output_format", "txt"])        
                print("Processing stdout....:  ",filename)  
        self.global_utility.merge_text_files(chunk_directory,chunks,filename)