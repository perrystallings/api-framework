from framework.core.server.base import create_server

app = create_server(spec_dir='/apps/app/schemas/', sync=True)
application = app.app
