from fastapi import APIRouter, HTTPException
import pandas as pd

router = APIRouter()

@router.post("/candidate-file-processor", response_model=FileProcessingResponse)
async def candidate_file_processor(fileProcessingRequest : FileProcessingReqquest):

    import pandas as pd

    # Load the file
    inputData = FileProcessingReqquest
    data = pd.read_json(inputData)

    # Display the original data
    print("Original Data: ", data.head())

    # Sort Data
    sortData = data.sort_values(by="能力試験JLPT", ascending=True)

    # Remove duplicate data
    delDupe = sortData.drop_duplicates()
    print(delDupe)

    #Convert rows to a list
    convDict = delDupe.to_dict(orient="list")
    print(convDict)

    return 0
