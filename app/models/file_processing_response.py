from pydantic import BaseModel, ConfigDict, root_validator, Field
from typing import List, Optional
from fastapi import HTTPException

class Candidate(BaseModel):
    id: Optional[int]
    age: Optional[int]
    birthday: Optional[str]
    currentAffiliation: Optional[str]
    japaneseLevel: Optional[str]
    jlpt: Optional[str]
    englishLevel: Optional[str]
    schoolLocation: Optional[str]
    schoolName: Optional[str]
    faculty: Optional[str]
    specialization: Optional[str]

class FileProcessingResponse(BaseModel):
    candidates: List[Candidate]