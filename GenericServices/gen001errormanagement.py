from Models.models import *
from .serializers import *


def gen001errormanagement(errId, request):
    # Fetch the error code and language from the request data
    language = request.get("userLanguage", "EN")

    # Fetch the error message from the error_codes table
    try:
        error = ErrorCode.objects.using("db999").get(
            error_code=errId, error_language=language)
        err_msg = error.error_message
    except ErrorCode.DoesNotExist:
        # Try to fetch the error message for English if the message for the selected language is not found
        try:
            error = ErrorCode.objects.using("db999").get(
                error_code=errId, error_language='EN')
            err_msg = error.message
        except ErrorCode.DoesNotExist:
            err_msg = "Unknown error"

    # Return the error message
    return err_msg
