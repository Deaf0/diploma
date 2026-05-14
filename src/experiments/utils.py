import hashlib


def enrich_result(result: dict, case_data: dict, case_id: int, repeat_id: int, elapsed: float) -> dict:
    result["A_name"] = case_data["A_name"]
    result["B_name"] = case_data["B_name"]
    result["case"] = case_id
    result["repeat_id"] = repeat_id
    result["time"] = elapsed
    return result


def build_error_message(experiment: str, case: int, method: str, total_points: int, error_message: str) -> dict:
    error_dict = dict()

    error_dict["experiment"] = experiment
    error_dict["case"] = case
    error_dict["method"] = method
    error_dict["total_points"] = total_points
    error_dict["error_message"] = str(error_message)
    return error_dict


def stable_seed(*args) -> int:
    return int(hashlib.md5("_".join(map(str, args)).encode()).hexdigest()[:8], 16)