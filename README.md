# rag_on_prem
This a Rag system using qdrand as vectordb and a GGUF model (quantized) as a GenAI


For use this project, after the clone you have to install some dependencies.

Steps:
- Install Python
- Install Llama.cpp
- Install python dependencies
- Download a quantized GenAI model
- Set environment variables
- run

In details
- Install Python --> https://www.python.org/ --> Python 3.10 could be ok
- Install Llama.cpp --> https://github.com/ggerganov/llama.cpp
  Inside the github page of llamacpp you can find all the steps for install it.
  You should clone it and build it (there is a different steps if you use Linux or Windows)
- Install python dependencies --> using pip you need to do "pip install -r requirements.txt" from the folder of the project
- Download a quantized GenAI model --> https://huggingface.co/TheBloke, in this page of HuggingFace you can find a lot of       quantized models (GGUF extension), an example can be this: https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF, go to "Files and versions" and you can download a .gguf model
- Set environment variables --> MODEL_PATH = "path_to_GGUF_model"
- run --> go to the project folder using bash and digit "python application.py"

Route
This project allow 3 differents route:
- /rag/ingestion: Need just one field inside the body: path_input_files --> can be the path of a 'txt' or 'pdf' file, or a path of a folder that contains some files ('pdf' or 'txt'). This route is able to load the content of the file(s), split it and, using a sentence trasformer, load it inside a vector DB
- /rag/inference: Need just one field inside the body: query --> should be the query for the GenAI. This route is able to search for the relevant documents, give the relevant documents as context with the input query as a question to GenAI and give a response to the user
- /rag/inference_without_ingestion: Need just one field inside the body: query --> should be the query for the GenAI. This route is able to ask the input query as a question to GenAI and give a response to the user


The default ip is: '127.0.0.1' and the default port is: '5002'.


Example INGESTION request:
-   type: POST
-   address: http://127.0.0.01:5002/rag/ingestion
-   JSON Body: {
    "path_input_files": "/home/ubuntu/articolo.txt"
}

Example INFERENCE request:
-   type: POST
-   address: http://127.0.0.01:5002/rag/inference
-   JSON Body: {
    "query": "input query"
}

Example INFERENCE WITHOUT INGESTION request:
-   type: POST
-   address: http://127.0.0.01:5002/rag/inference_without_ingestion
-   JSON Body: {
    "query": "input query"
}


For any problem write to --> giusclav95@gmail.com
