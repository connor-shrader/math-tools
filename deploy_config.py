# deploy_config.py

# This file contains configurations that are specific to the deployment version and/or cannot
# be publically visible.

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')