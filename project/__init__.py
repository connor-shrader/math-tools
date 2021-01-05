# project / __init__.py

# This file creates the Flask app and does most of the setup.

from flask import Flask

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')

# If the local_config exists, use that. Otherwise, configuration values
# are set from deploy_config (which reads from environment variables).
try:
    app.config.from_object('local_config')
except:
    app.config_from_object('deploy_config')

# Register Flask blueprints

from project._core.views import core
app.register_blueprint(core)

from project._statistics.views import statistics
app.register_blueprint(statistics)