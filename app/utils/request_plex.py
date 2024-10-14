from app.utils.handler_exceptions import handle_exceptions


def get_request(func, request=None):
    try:
        response = func(request=request) if request else func()
        return response
    except Exception as e:
        handle_exceptions(e)
