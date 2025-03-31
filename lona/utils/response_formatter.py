def format_success_response(data, message="Success"):
    return {
        "status": "success",
        "message": message,
        "data": data
    }

def format_error_response(error_message, status_code=400):
    return {
        "status": "error",
        "message": error_message,
        "code": status_code
    }

def format_response(data=None, error_message=None, status_code=200):
    if error_message:
        return format_error_response(error_message, status_code)
    return format_success_response(data)