def create_server(spec_dir, port=8080, debug=False):
    import connexion
    import os, yaml
    app = connexion.FlaskApp(__name__, port=port, specification_dir=spec_dir, debug=debug)

    for spec in os.listdir(spec_dir):
        app.add_api(specification=spec, validate_responses=debug)

    framework_schema_dir = os.path.abspath(__file__).replace('base.py', 'schemas/')
    for spec_file in os.listdir(framework_schema_dir):
        with open(os.path.join(framework_schema_dir, spec_file), 'rt') as f:
            spec = yaml.safe_load(f)
            app.add_api(specification=spec, validate_responses=debug)
    return app
