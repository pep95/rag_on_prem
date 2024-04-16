import pdb

from config import Settings
from pathlib import Path
import os
import fitz # install using: pip install PyMuPDF
from app.llm.service.utilities.utility import split_text_equally
from app.llm.service.preprocessing.data_preprocessing import text_cleaning
settings = Settings()

MANAGED_EXTENSION = settings.MANAGED_EXTENSION
###ingestion code

def open_current_file(path_file, extension):
    #pdb.set_trace()
    if extension.lower() == '.pdf':
        with fitz.open(path_file) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
    else:
        file = open(path_file, "r")
        text = file.read()
        file.close()
    return text

def get_lists_of_text(path):
    #pdb.set_trace()
    txt_files = []
    if Path(path).is_dir():
        list_files = os.listdir(path)
        for file in list_files:
            filename, file_extension = os.path.splitext(os.path.join(path, file))
            if file_extension in MANAGED_EXTENSION:
                text_current = open_current_file(os.path.join(path, file), file_extension)
                txt_files.append(text_current)


    else:
        filename, file_extension = os.path.splitext(path)
        if file_extension in MANAGED_EXTENSION:
            text_current = open_current_file(path, file_extension)
            txt_files.append(text_current)
    return txt_files

def split_and_preprocess_text(txt_files):
    txt_files_splitted = []
    txt_files_splitted_and_preprocessed = []
    for txt in txt_files:
        chunks = split_text_equally(txt)

        for chunk in chunks:
            txt_files_splitted.append(chunk)
            txt_files_splitted_and_preprocessed.append(text_cleaning(chunk))
    return txt_files_splitted, txt_files_splitted_and_preprocessed

def run_ingestion(path, vectordb):
    txt_files = get_lists_of_text(path)
    #print(txt_files)

    txt_files_splitted, txt_files_splitted_and_preprocessed = split_and_preprocess_text(txt_files)
    #pdb.set_trace()
    try:
        vectordb.run_ingestion(txt_files_splitted_and_preprocessed, txt_files_splitted)
        return True
    except:
        return False
