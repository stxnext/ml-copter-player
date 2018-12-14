import os.path

import controllers


def setup_routes(app):
    app.router.add_static(
        '/assets',
        os.path.join(os.path.dirname(__file__), 'static', 'assets'),
        name='static_assets'
    )
    app.router.add_static(
        '/js',
        os.path.join(os.path.dirname(__file__), 'static', 'js'),
        name='static_js'
    )
    app.router.add_get('/', controllers.index)
    app.router.add_get('/predict', controllers.websocket_handler)
    app.router.add_route('OPTIONS', '/sensors', controllers.preflight)
    app.router.add_post('/sensors', controllers.store_sensors_data)
    app.router.add_get('/generate_map', controllers.generate_map)
