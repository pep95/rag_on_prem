import os
import json
import pdb
import time
import pickle
import logging


from common.logger import logging_setup
from fastapi import APIRouter, Response
from llama_cpp import Llama
# **********************
# IMPORT PROJECT MODULES
# **********************
from app.llm.service.pipelines.inference_pipeline import inference_pipeline, inference_without_ingestion_pipeline
from app.llm.service.pipelines.ingestion_pipelines import run_ingestion
from config import Settings
from app.llm.service.validator.request_validator import IngestField, PredField
from app.llm.service.vectordb.qdrant_db import IngestionHandler

settings = Settings()

MODEL_PATH = settings.MODEL_PATH

router = APIRouter(prefix=f"{settings.PREFIX}", tags=[""])

# Logger configuration
logging_setup.setup_logging()
logger = logging.getLogger()

def load_model():
    llm = Llama(
        model_path=MODEL_PATH,  # Download the model file first
        n_ctx=2048,  # The max sequence length to use - note that longer sequence lengths require much more resources
        n_threads=8,  # The number of CPU threads to use, tailor to your system and the resulting performance
        n_gpu_layers=35  # The number of layers to offload to GPU, if you have GPU acceleration available
    )
    return llm

try:
    llm = load_model()
    logger.info('LLm MODEL SUCCESSFULLY LOADED')

    vectordb = IngestionHandler()


except Exception as e:
    logger.error('ERROR INITIALIZING THE SERVICE', exc_info=e)



@router.get('/')
async def healthcheck():
    return Response(json.dumps({'Status': 'Available'}),
                    status_code=200,
                    media_type='application/json')

@router.post('/ingestion')
async def prediction_service_skip(item: IngestField):
    """
    This function manages the ingestion requests.

    Parameters
    ----------
    item: IngestField
        IngestField object for mapping the incoming request and validating it

    Returns
    -------
    response_json : Response
        JSON response for ingestion pipeline
    """

    try:
        start_prediction_time = time.time()
        logger.info('Ingestion service started.')
        request_json = item.dict()
        response = run_ingestion(request_json['path_input_files'], vectordb)
        # Prediction service response
        if response is True:
            response_service = dict(detail={'msg': 'Ingestion OK'})
            logger.info("Ingestion OK")
            return Response(json.dumps(response_service), media_type='application/json')
        else:
            logger.error(f"Ingestion error")
            response_service = dict(detail={'msg': 'Ingestion error'})
            return Response(json.dumps(dict(detail={'msg': 'Ingestion error'})),
                            status_code=500, media_type='application/json')

    except Exception as e:
        logger.error('PREDICTION ERROR', exc_info=e)


@router.post('/inference')
async def prediction_service_skip(item: PredField):
    """
    This function manages the ingestion requests.

    Parameters
    ----------
    item: PredField
        PredField object for mapping the incoming request and validating it

    Returns
    -------
    response_json : Response
        JSON response for model pipeline
    """

    try:
        start_prediction_time = time.time()
        logger.info('Inference service started.')
        request_json = item.dict()
        text_output = inference_pipeline(request_json['query'], llm, vectordb)
        # Prediction service response
        if text_output is not None:
            response_service = dict(detail={'msg': f'{text_output}'})
            logger.info("Inference OK")
            return Response(json.dumps(response_service), media_type='application/json')
        else:
            logger.error(f"Inference error")
            response_service = dict(detail={'msg': 'Inference error'})
            return Response(json.dumps(dict(detail={'msg': 'Inference error'})),
                            status_code=500, media_type='application/json')

    except Exception as e:
        logger.error('PREDICTION ERROR', exc_info=e)


@router.post('/inference_without_ingestion')
async def prediction_service_skip(item: PredField):
    """
    This function manages the ingestion without ingestion requests.

    Parameters
    ----------
    item: PredField
        PredField object for mapping the incoming request and validating it

    Returns
    -------
    response_json : Response
        JSON response for model without ingestion pipeline
    """

    try:
        start_prediction_time = time.time()
        logger.info('Inference without ingestion service started.')
        request_json = item.dict()
        text_output = inference_without_ingestion_pipeline(request_json['query'], llm)
        # Prediction service response
        if text_output is not None:
            response_service = dict(detail={'msg': f'{text_output}'})
            logger.info("Inference without ingestion OK")
            return Response(json.dumps(response_service), media_type='application/json')
        else:
            logger.error(f"Inference error")
            response_service = dict(detail={'msg': 'Inference without ingestion error'})
            return Response(json.dumps(dict(detail={'msg': 'Inference error'})),
                            status_code=500, media_type='application/json')

    except Exception as e:
        logger.error('PREDICTION ERROR', exc_info=e)
