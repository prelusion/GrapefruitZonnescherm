import time


def retry_on_any_exception(retries, sleep=0, ignored=None):
    """
    :param retries:
    :param sleep:
    :param ignored: single exception or tuple / list of exceptions
    :return:
    """
    if not isinstance(ignored, tuple) and not isinstance(ignored, list):
        ignored = (ignored,)

    def decorator(fn):
        def wrapper(*args, **kwargs):

            for i in range(retries):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    if e.__class__ in ignored:
                        raise

                    if i < retries - 1:
                        if sleep > 0:
                            time.sleep(sleep)
                        continue

                    raise

        return wrapper
    return decorator


def retry_on_given_exception(exceptions, retries, sleep=0):

    if not isinstance(exceptions, tuple) and not isinstance(exceptions, list):
        exceptions = (exceptions,)

    def decorator(fn):

        def wrapper(*args, **kwargs):

            for i in range(retries):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    print("Exception:", e)
                    print("RETRY")
                    if e.__class__ not in exceptions:
                        raise

                    if i < retries - 1:
                        if sleep > 0:
                            time.sleep(sleep)
                        continue

                    raise

        return wrapper
    return decorator
