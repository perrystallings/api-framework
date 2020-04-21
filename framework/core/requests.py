__client_session__ = None


def get_client_session():
    import aiohttp
    global __client_session__
    if __client_session__ is None:
        __client_session__ = aiohttp.ClientSession()
    return __client_session__


def make_sync_request(method, url, **kwargs):
    import requests
    from requests.exceptions import ConnectionError, HTTPError
    js = dict()
    status_code = None
    try:
        response = requests.request(method=method, url=url, **kwargs)
    except ConnectionError as exc:
        pass
    else:
        status_code = response.status_code
        try:
            response.raise_for_status()
        except HTTPError as exc:
            js = format_response_body(response=response)
        else:
            js = format_response_body(response=response)


async def make_async_request(method, url, **kwargs):
    import aiohttp
    session = get_client_session()
    status = None
    async with session.request(method=method, url=url, **kwargs) as resp:
        try:
            await resp.read()
        except aiohttp.ClientError as e:
            js = format_response_body(response=resp)
        else:
            status = resp.status
            js = format_response_body(response=resp)
    return status, js


def safe_json_request(method, url, **kwargs):
    """Convenience function for calling external APIs to simplify error handling.

    :param method: HTTP methond (GET, POST, PUT, etc.)
    :param url: Request URL.
    :param kwargs: Additional parameters. See requests.request for details.
    :return: tuple of status_code and json body as a python dict
    """
    import asyncio
    if asyncio.get_event_loop().is_running():
        return await make_async_request(method=method, url=url, **kwargs)
    else:
        return make_sync_request(method=method, url=url, **kwargs)


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
