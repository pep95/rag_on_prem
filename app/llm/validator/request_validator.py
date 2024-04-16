from pydantic import BaseModel, validator
from config import Settings
from typing import Optional, Union
from fastapi import HTTPException
import logging
from common.logger import logging_setup
from pathlib import Path



settings = Settings()

# Logger configuration
logging_setup.setup_logging()
logger = logging.getLogger()


class IngestField(BaseModel):
    path_input_files: Optional[Union[str, int, float, list, tuple, bytes, dict, bool, set]]

    @validator('path_input_files', always=True)
    def path_input_files_val(cls, v):
        if v is None:
            error_response = {
                "msg": f"path_input_files cannot be null"
            }
            logger.error(f"Validation error: {error_response['msg']}")
            raise HTTPException(status_code=422, detail=error_response)

        if type(v) is not str:
            error_response = {
                "msg": f"path_input_files must be str, not {type(v).__name__}"
            }
            logger.error(f"Validation error: {error_response['msg']}")
            raise HTTPException(status_code=422, detail=error_response)

        if not ((Path(v).exists()) or (Path(v).is_dir())):
            error_response = {
                "msg": f"path_input_files must be a path of file or a path of a folder"
            }
            logger.error(f"Validation error: {error_response['msg']}")
            raise HTTPException(status_code=422, detail=error_response)
        return v
class PredField(BaseModel):
    query: Optional[Union[str, int, float, list, tuple, bytes, dict, bool, set]]

    @validator('query', always=True)
    def query_val(cls, v):
        if v is None:
            error_response = {
                "msg": f"query cannot be null"
            }
            logger.error(f"Validation error: {error_response['msg']}")
            raise HTTPException(status_code=422, detail=error_response)

        if type(v) is not str:
            error_response = {
                "msg": f"query must be str, not {type(v).__name__}"
            }
            logger.error(f"Validation error: {error_response['msg']}")
            raise HTTPException(status_code=422, detail=error_response)

        return v
