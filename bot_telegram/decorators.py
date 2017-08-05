from functools import wraps


def initial_message_on_error(wrapped):
    @wraps(wrapped)
    async def wrapper(*args, **kwargs):
        try:
            return await wrapped(*args, **kwargs)
        except:
            return

    return wrapper
