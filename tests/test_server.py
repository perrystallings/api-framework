import pytest


@pytest.fixture()
def client(test_directory):
    import os
    from framework.core.server import create_server
    app = create_server(spec_dir=os.path.join(test_directory, 'mocks/example_app/schemas'))
    return app.app.test_client()


def test_template_home(client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_template_api_ui(client):
    resp = client.get('v1/ui/')
    assert resp.status_code == 200


def test_template_api_example(client):
    resp = client.get('v1/hello', headers=dict(Authorization='Bearer test'))
    assert resp.status_code == 200


def custom_health_check():
    return dict(status="this is a test")


def test_custom_health_check(test_directory):
    from framework.core.server import create_server

    import os
    client = create_server(
        spec_dir=os.path.join(test_directory, os.path.join(test_directory, 'mocks/example_app/schemas')),
        custom_home=custom_health_check
    ).app.test_client()
    resp = client.get('/')
    assert resp.json == custom_health_check()


def test_package_apis(test_directory):
    from framework.core.server import create_server
    import os
    import shutil
    new_package_dir = os.path.join(test_directory, '../framework/example_package')
    shutil.copytree(os.path.join(test_directory, 'mocks/example_package/'), new_package_dir)
    client = create_server(
        spec_dir=os.path.join(test_directory, os.path.join(test_directory, 'mocks/example_app/schemas')),
        custom_home=custom_health_check

    ).app.test_client()
    js = dict(head=1)
    assert client.post('package/v1/echo', json=js).json == js
    shutil.rmtree(new_package_dir)
