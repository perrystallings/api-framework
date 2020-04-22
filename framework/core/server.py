def create_server(spec_dir, port=8080, debug=False):
    import connexion
    import os
    import yaml

    app = connexion.FlaskApp(__name__, port=port, specification_dir=spec_dir, debug=debug)

    for spec in os.listdir(spec_dir):
        app.add_api(specification=spec, validate_responses=debug)

    framework_dir = os.path.abspath(__file__).replace('/core/server.py', '/')

    for root, folders, files in os.walk(framework_dir):
        if 'schemas' in root and 'template' not in root:
            for spec_file in [i for i in files if 'yaml' in i]:
                with open(os.path.join(root, spec_file), 'rt') as f:
                    spec = yaml.safe_load(f)
                app.add_api(specification=spec, validate_responses=debug)
    return app
