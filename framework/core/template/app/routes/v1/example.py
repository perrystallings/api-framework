def post_json_example(body: dict) -> dict:
    """Sample API handler that accepts a json body

    :param body: the json body variable
    :return: dictionary containing a single "value" parameter
    """
    from framework.core.requests import get_request_access_token
    return dict(value=True, token=get_request_access_token())
