from flask import Flask

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')

try:
    app.config.from_object('local_config')
except:
    app.config_from_object('deploy_config')

from project._core.views import core
app.register_blueprint(core)

from project._statistics.views import statistics
app.register_blueprint(statistics)