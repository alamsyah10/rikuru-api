from typing import List
from fastapi import HTTPException
import ast
from app.models.file_processing_request import Candidate
from app.services.chatgpt_service import call_gpt

def candidate_sorting_service(candidates: List[Candidate], priorities: List[str]) -> List[Candidate]:
    convert_dict = {
        "能力試験JLPT": "jlpt",
        "学校名": "schoolName"
    }
    for priority in priorities:
        data = list({getattr(item, convert_dict[priority]) for item in candidates})
        prompt = ""
        if (convert_dict[priority] == "schoolName"):
            prompt = f"""
            Based on this "data", please sort the universities by ranking and provide the response in the following format, also Please write the response in the defined format without adding any extra text and makes sure the sorted data doesn't removed or changed the original data, makes sure all the data included in your

            data : {data}

            response format: 
            [
                "Univ A",
                "Univ B",
                "Univ C",
            ]
            """
        if (convert_dict[priority] == "jlpt"):
            prompt = f"""
            Based on this "data", please sort the japanese profficiency level from the highest jlpt level and provide the response in the following format, also please write the response in the defined format without adding any extra text

            data : {data}

            response format: 
            [
                "N1",
                "N2",
                "N3",
            ]
            """
        identity = "You are a recruiter from Japanese company that want to hire foreigner engineer, make decision based on this identity"
        response = ast.literal_eval(call_gpt(prompt, identity)["response"]) 
        print(f"data: {data}")
        print(f"len data: {len(data)}")
        print(f"len response: {len(response)}")
        print(f"response: {response}")
    print(data)
    return candidates
