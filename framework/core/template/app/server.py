from framework.core.server import create_server
import os

app = create_server(spec_dir=os.path.join(os.path.abspath(__file__).replace('server.py', ''), './schemas/'))
application = app.app


@app.route('/')
def health_check():
    return "ok"
