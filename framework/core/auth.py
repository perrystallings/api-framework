__auth_keys__ = None


def get_audience(service_name=None) -> str:
    from framework.core.settings import get_app_settings
    app_settings = get_app_settings()
    if not service_name:
        service_name = app_settings['service_name']
    if app_settings['auth_domain'] == "https://adara-poc.auth0.com":
        env = 'qa'
    elif app_settings['auth_domain'] == "https://adara.auth0.com":
        env = 'prod'
    else:
        raise ValueError("Not Valid Auth Domain")
    audience = 'https://{0}-{1}.adara.com'.format(
        service_name, env
    )
    return audience


def get_auth_keys():
    from framework.core.requests import safe_json_request
    from framework.core.settings import get_app_settings
    app_settings = get_app_settings()
    global __auth_keys__
    if __auth_keys__ is None:
        status_code, js = safe_json_request(method='GET',
                                            url="{0}/.well-known/jwks.json".format(app_settings['auth_domain']))
        if js:
            __auth_keys__ = js['keys']
    return __auth_keys__


def decode_token(token, auth_keys):
    from jose import jwt
    from framework.core.settings import get_app_settings
    app_settings = get_app_settings()

    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    payload = None
    user_token = False
    for key in auth_keys:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=get_audience(),
                issuer='{0}/'.format(app_settings['auth_domain'])
            )
        except jwt.JWTError:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=app_settings.get('app_domain', 'https://login.adara.com'),
                    issuer='{0}/'.format(app_settings.get('custom_auth_issuer', app_settings['auth_domain']))
                )
            except jwt.JWTError:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=app_settings.get('app_domain', 'https://login.adara.com'),
                    issuer='{0}/'.format(app_settings['auth_domain'])
                )
            if payload['sub'].startswith('auth0'):
                user_token = True
    return user_token, payload


# def get_user_scopes(user_token=None, user=None, service_name=None):
#     from handlers.core.common import safe_json_request, generate_oauth_headers
#     from handlers.core.auth import get_service_access_token, get_audience
#     from server import app_settings, logger
#     scopes = []
#     if service_name is None:
#         service_name = app_settings['service_name']
#     audience = get_audience(service_name=service_name)
#     if user_token is not None:
#         status_code, js = safe_json_request(
#             method='post',
#             url="{0}{1}".format(app_settings['user_service_domain'], app_settings['validate_scopes_path']),
#             headers=generate_oauth_headers(
#                 access_token=user_token
#             ),
#             json=dict(
#                 audience=audience,
#                 scopes=[]
#             )
#         )
#         if status_code == 200:
#             scopes = js['response'].get('available_scopes', [])
#     elif user is not None:
#         token = get_service_access_token(service_name='user')
#         status_code, js = safe_json_request(
#             method='post', url="{0}{1}".format(app_settings['user_service_domain'], app_settings['user_scopes_path']),
#             headers=generate_oauth_headers(
#                 access_token=token
#             ),
#             json=dict(
#                 audience=audience,
#                 user_id=user
#             )
#         )
#         if status_code == 200:
#             scopes = js['response'].get('scopes', [])
#
#     return " ".join(scopes)


def verify_token(token):
    from jose import jwt
    from werkzeug.exceptions import Unauthorized
    from aiohttp.web_exceptions import HTTPUnauthorized
    import asyncio
    import six
    keys = get_auth_keys()

    if not keys:
        raise Unauthorized
    try:
        user_token, decoded_token = decode_token(token=token, auth_keys=keys)
    except jwt.JWTError as e:
        if asyncio.get_event_loop().is_running():
            six.raise_from(HTTPUnauthorized, e)
        else:
            six.raise_from(Unauthorized, e)
    else:
        return decoded_token


def verify_auth(username, password, required_scopes=None):
    return {'sub': username, 'scope': ''}


# def handle_user_token_request(user, body):
#     from server import app_settings
#     from connexion import request
#     from handlers.core.common import safe_json_request
#     from handlers.core.auth import get_audience
#
#     js = dict(
#         client_id=user,
#         client_secret=request.authorization.password,
#         audience=get_audience(),
#         **body
#     )
#
#     status_code, js = safe_json_request(
#         url=app_settings['auth_url'], method='POST',
#         json=js
#     )
#     return js, status_code


def validate_request():
    import asyncio
    if asyncio.get_event_loop().is_running():
        return
