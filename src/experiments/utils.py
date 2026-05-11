def enrich_result(result: dict, case_data: dict, case_id: int, elapsed: float) -> dict:
    result["A_name"] = case_data["A_name"]
    result["B_name"] = case_data["B_name"]
    result["case"] = case_id
    result["time"] = elapsed
    return result