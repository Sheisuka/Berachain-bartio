import settings


def exception_handler(func, retries:int = settings.RETRIES_COUNT):
    def wrapper(*args, **kwargs):
        for retry in range(retries):
            try:
                print("Doing func")
                func(*args, **kwargs)
                return
            except Exception as error:
                raise error
    return wrapper