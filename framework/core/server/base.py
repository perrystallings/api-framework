def create_server(spec_dir, port=8080, debug=False):
    import connexion
    import os
    # configure_logging(log_level=server_settings.get('log_level', 'INFO'))
    app = connexion.FlaskApp(__name__, port=port, specification_dir=spec_dir, debug=debug)
    # Read the config files to configure the endpoints
    for spec in os.listdir(spec_dir):
        app.add_api(specification=spec, validate_responses=debug)
    return app
