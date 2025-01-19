from fastapi import APIRouter, HTTPException
import pandas as pd

router = APIRouter()

@router.post("/candidate-file-processor", response_model=FileProcessingResponse)
async def candidate_file_processor(fileProcessingRequest : FileProcessingReqquest):

    # Load the Excel file
    file_path = "data.xlsx"  # Replace with your file path
    sheet_name = "Sheet1"  # Replace with your sheet name
    data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Display the first few rows of the data (optional)
    print("Original Data:")
    print(data.head())

    # Apply a filter (e.g., selecting rows where "Age" is greater than 30)
    filtered_data = data[data["Age"] > 30]

    # Display the filtered data (optional)
    print("\nFiltered Data:")
    print(filtered_data)

    # Save the filtered data to a new Excel file
    output_file_path = "filtered_data.xlsx"
    filtered_data.to_excel(output_file_path, index=False)

    print(f"\nFiltered data saved to {output_file_path}")

    return 0
