__app_settings__ = None


def load_app_settings():
    import os, json
    from os import path
    global __app_settings__
    from framework.core.common import generate_random_id
    import logging
    if __app_settings__ is None:
        app_settings = dict()
        env_folder = os.getenv('ENV_FOLDER', '/apps/settings/')

        for root, folder, files in os.walk(env_folder):
            for file in files:
                local_path = path.join(env_folder, '{0}/{1}.json'.format(folder, file))
                try:
                    with open(local_path, 'rt') as f:
                        app_settings.update(json.load(f))
                except (IOError, json.JSONDecodeError) as e:
                    logging.error(local_path)
                    raise e
        prefix = ''
        if app_settings.get('environment', 'test') == 'test':
            prefix = generate_random_id().split('-')[0]
        app_settings['prefix'] = prefix
        __app_settings__ = {k: format_setting_value(v) for k, v in app_settings.items()}

    return __app_settings__


def format_setting_value(value):
    import json
    import logging
    formatted_value = value
    if any([i in value for i in ['"', '[', '{']]):
        try:
            formatted_value = json.loads(value)
        except json.JSONDecodeError as exc:
            logging.debug(exc)
    return formatted_value
