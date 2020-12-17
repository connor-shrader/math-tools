from flask import Flask

app = Flask(__name__, instance_relative_config=True)

ENV = 'dev'

'''
if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:!1connor!!!@localhost/shrader-management-systems-test'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

db = SQLAlchemy(app)
'''



app.config.from_object('config')
app.config.from_pyfile('config.py')

from project._core.views import core
app.register_blueprint(core)

from project._statistics.views import statistics
app.register_blueprint(statistics)