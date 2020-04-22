def post_json_example(user, token_info, body: dict) -> dict:
    """Sample API handler that accepts a json body

    :param body: the json body variable
    :return: dictionary containing a single "value" parameter
    """
    print(body)
    return dict(value=True)
