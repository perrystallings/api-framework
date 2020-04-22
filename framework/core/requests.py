def get_request_headers():
    from connexion import request
    try:
        headers = request.headers
    except RuntimeError:
        headers = None
    return headers


def generate_oauth_headers(access_token: str) -> dict:
    """Convenience function to generate oauth stand authorization header

    :param access_token: Oauth access token
    :return: Request headers
    """
    return {'Authorization': 'Bearer ' + access_token}


def get_request_access_token():
    headers = get_request_headers()
    token = None
    if headers is not None and headers.get('Authorization') is not None:
        token = headers['Authorization'].split(' ')[-1]
    return token


def safe_json_request(method, url, retry=False, **kwargs):
    """Convenience function for calling external APIs to simplify error handling.

    :param method: HTTP methond (GET, POST, PUT, etc.)
    :param url: Request URL.
    :param kwargs: Additional parameters. See requests.request for details.
    :return: tuple of status_code and json body as a python dict
    """
    import requests
    from requests.exceptions import ConnectionError, HTTPError
    from logging import getLogger
    logger = getLogger()
    js = dict()
    status_code = None
    try:
        response = requests.request(method=method, url=url, **kwargs)
    except ConnectionError as exc:
        logger.error(exc)
    else:
        status_code = response.status_code
        logger.info(
            dict(method=method, url=url, status_code=response.status_code, elapsed=response.elapsed))
        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code >= 500 and not retry:
                status_code, js = safe_json_request(method=method, url=url, retry=True, **kwargs)
            else:
                logger.error(exc)
                js = format_response_body(response=response)
                logger.error(js)
        else:
            js = format_response_body(response=response)

    return status_code, js


def format_response_body(response):
    js = dict()
    try:
        js = response.json()
    except ValueError:
        if callable(response.text):
            js['content'] = response.text()
        if callable(response.text):
            js['content'] = response.text
    return js
