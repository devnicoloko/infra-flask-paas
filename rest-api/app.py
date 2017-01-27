import logging
from rabbitmq_publisher import launch_rabbitmq, configure
from flask import Flask, request
from flasgger import Swagger
from routes_vm import routes_vm
from routes_main import routes_main
from routes_connect import routes_connect

app = Flask(__name__)
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "0.0.1",
            "title": "RET PaaS Automation Beta",
            "endpoint": 'v1_spec',
            "route": '/v1/spec',
        }
    ]
}
Swagger(app)


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                '-35s %(lineno) -5d: %(message)s')

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

app.register_blueprint(routes_vm, url_prefix='/v1/vm')
app.register_blueprint(routes_main, url_prefix='/v1')
app.register_blueprint(routes_connect, url_prefix='/v1')

launch_rabbitmq.start()
configure()

app.run(debug=True,host='0.0.0.0')


