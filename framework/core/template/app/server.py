from framework.core.server import create_server
import os

current_directory = os.path.abspath(__file__).replace('server.py', '')

app = create_server(
    spec_dir=os.path.join(current_directory, './schemas/'), debug=False
)
application = app.app
