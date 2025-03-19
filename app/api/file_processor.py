from fastapi import APIRouter, HTTPException
from app.models.file_processing_request import FileProcessingRequest, Candidate
from app.models.file_processing_response import FileProcessingResponse
import pandas as pd

router = APIRouter()

@router.post("/candidate-file-processor", response_model=FileProcessingResponse)
async def candidate_file_processor(request: FileProcessingRequest):
    print(f"request: {request}")
    
    # Convert the list of candidates to a DataFrame
    candidates_data = pd.DataFrame([candidate.dict() for candidate in request.candidates])

    # Display the original data
    print("Original Data: ", candidates_data.head())

    # Sort Data by 'jlpt'
    sort_data = candidates_data.sort_values(by="jlpt", ascending=True)

    # Remove duplicate data
    del_dupe = sort_data.drop_duplicates()
    print(del_dupe)

    # Convert rows to a list of dictionaries
    conv_dict = del_dupe.to_dict(orient="list")
    print(conv_dict)

    candidates = [
        {
            "id": conv_dict['id'][i] if i < len(conv_dict['id']) else None,
            "age": conv_dict['age'][i] if i < len(conv_dict['age']) else None,
            "birthday": conv_dict['birthday'][i] if i < len(conv_dict['birthday']) else None,
            "currentAffiliation": conv_dict['currentAffiliation'][i] if i < len(conv_dict['currentAffiliation']) else None,
            "japaneseLevel": conv_dict['japaneseLevel'][i] if i < len(conv_dict['japaneseLevel']) else None,
            "jlpt": conv_dict['jlpt'][i] if i < len(conv_dict['jlpt']) else None,
            "englishLevel": conv_dict['englishLevel'][i] if i < len(conv_dict['englishLevel']) else None,
            "schoolLocation": conv_dict['schoolLocation'][i] if i < len(conv_dict['schoolLocation']) else None,
            "schoolName": conv_dict['schoolName'][i] if i < len(conv_dict['schoolName']) else None,
            "faculty": conv_dict['faculty'][i] if i < len(conv_dict['faculty']) else None,
            "specialization": conv_dict['specialization'][i] if i < len(conv_dict['specialization']) else None
        }
        for i in range(len(conv_dict['id']))
    ]

    return FileProcessingResponse(candidates=candidates)
