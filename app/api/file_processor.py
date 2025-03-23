from fastapi import APIRouter, HTTPException
from app.models.file_processing_request import FileProcessingRequest, Candidate
from app.models.file_processing_response import FileProcessingResponse
from app.services.sorting_service import candidate_sorting_service
import pandas as pd

router = APIRouter()

@router.post("/candidate-file-processor", response_model=FileProcessingRequest)
async def candidate_file_processor(request: FileProcessingRequest):
    sorted_data = candidate_sorting_service(request.candidates, request.priorities)
    response = FileProcessingRequest(candidates=sorted_data, priorities=request.priorities)
    # print(f"request: {request.priorities}")
    return response
