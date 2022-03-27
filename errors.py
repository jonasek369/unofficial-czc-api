def throw_json_error():
    return {
        "status": "ERROR",
        "message": "There was an error in json"
    }


def throw_missing_parameters(parameters):
    return {
        "status": "ERROR",
        "message": f"There was an error in json. Missing parameters: {parameters}"
    }
