def create_server(spec_dir, sync: bool = False, port=8080, debug=False):
    import connexion
    import os
    # configure_logging(log_level=server_settings.get('log_level', 'INFO'))
    if sync:
        app = connexion.FlaskApp(__name__, port=port, specification_dir=spec_dir, debug=debug)
    else:
        app = connexion.AioHttpApp(__name__, port=8080, specification_dir=spec_dir, debug=True)
    # Read the config files to configure the endpoints
    for spec in os.listdir(spec_dir):
        app.add_api(specification=spec, validate_responses=debug)
    return app
