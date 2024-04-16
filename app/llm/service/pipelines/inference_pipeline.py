import pdb

from app.llm.service.utilities.utility import create_prompt_without_context, create_prompt_with_context
from app.llm.service.model.ask_model import inference
from app.llm.service.pipelines.retrieving_pipeline import get_top_context
from config import Settings
settings = Settings()
PROMPT_WITHOUT_CONTEXT = settings.PROMPT_WITHOUT_CONTEXT
PROMPT_PATH_WITH_CONTEXT1 = settings.PROMPT_PATH_WITH_CONTEXT1
PROMPT_PATH_WITH_CONTEXT2 = settings.PROMPT_PATH_WITH_CONTEXT2
#
#
def inference_pipeline(query, llm, vectordb):
    context = get_top_context(query, vectordb)
    prompt = create_prompt_with_context(PROMPT_PATH_WITH_CONTEXT1, PROMPT_PATH_WITH_CONTEXT2, context, query)

    response = inference(llm, prompt)

    response = response['choices'][0]['text']
    response = response.split('[/INST]')[1]
    return response
#
def inference_without_ingestion_pipeline(query, llm):
    prompt = create_prompt_without_context(PROMPT_WITHOUT_CONTEXT, query)
    response = inference(llm, prompt)
    response = response['choices'][0]['text']
    response = response.split('[/INST]')[1]
    return response
