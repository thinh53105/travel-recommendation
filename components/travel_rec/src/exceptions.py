from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI


class RecordNotExists(Exception):
    pass


class UpstreamServiceUnavailable(Exception):
    def __init__(self, name) -> None:
        self.name = name


def configure_exception(app: FastAPI):
    app.add_exception_handler(RecordNotExists, record_not_exists_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(UpstreamServiceUnavailable,
                              upstream_service_unavailable_handler)


async def record_not_exists_handler(request, exc: RecordNotExists):
    return JSONResponse({
            'error': 'UID not found',
            'message': 'The provided UID does not exist. Please check the UID and try again.'
        }, status_code=404
    )

async def validation_error_handler(request, exc: ValidationError):
    first_error = exc.errors()[0]
    atr_name, msg = first_error['loc'][0], first_error['msg']
    message = f'`{atr_name}`: {msg}'
    return JSONResponse({'error': message}, status_code=400)

async def upstream_service_unavailable_handler(
        request, exc: UpstreamServiceUnavailable):
    return JSONResponse(
        {'error': f'Service `{exc.name}` unavailable!'}, status_code=503
    )
