from typing import List
from fastapi import HTTPException
import ast
from app.models.file_processing_request import Candidate
from app.services.chatgpt_service import call_gpt
import re
# Function to get the rank index or fallback to a large value if not found
def get_rank(value: str, ranking_list: List[str]) -> int:
    """Returns the index of the value in the ranking list or a large value if not found."""
    try:
        return ranking_list.index(value)
    except ValueError:
        return len(ranking_list)  # Unranked items go to the end

# Function to generate the sorting key with normalization
def get_sort_key(
    candidate: Candidate, 
    priorities: List[str], 
    JLPT_RANKING: List[str] = None, 
    SCHOOL_RANKING: List[str] = None
) -> tuple:
    
    # Initialize ranking scores
    jlpt_rank = None
    school_rank = None

    # Initialize normalized scores
    normalized_jlpt_score = None
    normalized_school_score = None

    # Get JLPT and school rankings
    if JLPT_RANKING is not None:
        jlpt_rank = get_rank(candidate.jlpt, JLPT_RANKING)
        normalized_jlpt_score = jlpt_rank / max(1, len(JLPT_RANKING) - 1)  # Normalize between 0 and 1

    if SCHOOL_RANKING is not None:
        school_rank = get_rank(candidate.schoolName, SCHOOL_RANKING)
        normalized_school_score = school_rank / max(1, len(SCHOOL_RANKING) - 1)  # Normalize between 0 and 1

    # Handle None values safely when calculating combined score
    combined_score = 0

    if normalized_jlpt_score is not None and normalized_school_score is not None:
        combined_score = (normalized_jlpt_score + normalized_school_score) / 2  # Average both scores
    elif normalized_jlpt_score is not None:
        combined_score = normalized_jlpt_score  # Only JLPT available
    elif normalized_school_score is not None:
        combined_score = normalized_school_score  # Only school available

    # Fallback to other priorities
    priority_keys = []
    for priority in priorities:
        value = getattr(candidate, priority, "")
        if priority == "jlpt":
            priority_keys.append(jlpt_rank if jlpt_rank is not None else float("inf"))  # Use infinity if missing
        elif priority == "schoolName":
            priority_keys.append(school_rank if school_rank is not None else float("inf"))
        else:
            priority_keys.append(value or "")

    # Add combined score as the primary sorting key
    return (combined_score, *priority_keys)

def get_string_with_brackets(s):
    match = re.search(r'(\[([^\]]+)\])', s)  # Regular expression to find content with brackets
    return match.group(1) if match else None

def candidate_sorting_service(candidates: List[Candidate], priorities: List[str]) -> List[Candidate]:
    convert_dict = {
        "能力試験JLPT": "jlpt",
        "学校名": "schoolName"
    }
    ranking = {}
    for priority in priorities:
        data = list({getattr(item, convert_dict[priority]) for item in candidates})
        prompt = ""
        loc = candidates[0].schoolLocation
        # sort univ by computer science -> by contest / by publikasi
        if (convert_dict[priority] == "schoolName"):
            prompt = f"""
            Based on this "data," please sort the universities by QS World University Rankings of {loc} from top ranking and provide the response in the following format. Ensure that:

            1. The response strictly follows the defined format without adding any extra text, not in json or any additional format.
            2. The original data is preserved, meaning no data is removed or altered.
            3. All the data is included in your response.
            4. Abbreviations and universities with the same name remain as separate entries, without being combined into one.

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
            Based on this "data", please sort the japanese profficiency level from the highest jlpt level and The response strictly follows the defined format without adding any extra text, not in json or any additional format

            data : {data}

            response format: 
            [
                "N1",
                "N2",
                "N3",
            ]
            """
        # identity = "You are a recruiter from Japanese company that want to hire foreigner engineer, make decision based on this identity"
        identity = ""
        gpt_response = call_gpt(prompt, identity)["response"]
        print("gpt response", gpt_response)
        response = ast.literal_eval(get_string_with_brackets(gpt_response)) 
        ranking[convert_dict[priority]] = response
        print(f"data: {data}")
        print(f"len data: {len(data)}")
        print(f"len response: {len(response)}")
        print(f"response: {response}")
    sorted_data = sorted(candidates, key=lambda c: get_sort_key(c, priorities, ranking.get('jlpt', None), ranking.get('schoolName', None)))
    
    fixed = []
    for data_index in range(len(sorted_data)):
        d = sorted_data[data_index]
        d.no = data_index + 1
        fixed.append(d)

    return fixed
