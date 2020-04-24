import pytest


@pytest.fixture()
def client():
    from framework.core.template.app.server import application
    return application.test_client()


def test_template_home(client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_template_api_ui(client):
    resp = client.get('v1/ui/')
    assert resp.status_code == 200


def test_template_api_example(client):
    resp = client.post('v1/example', json=dict(sub_object=dict(a=1)), headers=dict(Authorization='Bearer test'))
    assert resp.status_code == 200


def custom_health_check():
    return dict(status="this is a test")


def test_custom_health_check():
    from framework.core.server import create_server
    from framework.core.template.app.server import current_directory

    import os
    client = create_server(
        spec_dir=os.path.join(current_directory, './schemas/'),
        custom_home=custom_health_check
    ).app.test_client()
    resp = client.get('/')
    assert resp.json == custom_health_check()
