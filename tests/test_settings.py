def test_override_test_settings():
    import os
    from framework.core.settings import get_app_settings
    app_settings = get_app_settings(
        env_folder=os.path.join(os.path.abspath(__file__).replace('/tests/test_settings.py', ''),
                                'framework/core/template/deployment/settings'))
    assert app_settings['environment'] == 'test'
    assert app_settings['service_name'] == 'example'


def test_settings_parser_raises_error():
    import os
    import pytest
    from json import JSONDecodeError
    from framework.core.settings import get_app_settings
    pytest.raises(JSONDecodeError)
    app_settings = get_app_settings(
        env_folder=os.path.join(os.path.abspath(__file__).replace('/tests/test_settings.py', ''),
                                'framework/core/template/deployment/conf'))
    assert app_settings['environment'] == 'test'
    assert app_settings['service_name'] == 'example'


def test_load_json_object():
    from framework.core.settings import format_setting_value
    assert format_setting_value('{"test":"value"}') == dict(test='value')


def test_load_json_array():
    from framework.core.settings import format_setting_value
    assert format_setting_value('["test", "value"]') == ['test', 'value']


def test_load_json_string():
    from framework.core.settings import format_setting_value
    assert format_setting_value('"test"') == "test"


def test_load_non_json_string():
    from framework.core.settings import format_setting_value
    assert format_setting_value('"test') == '"test'
