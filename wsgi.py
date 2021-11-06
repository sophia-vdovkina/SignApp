import os
from env import env
env.configure_app()
from application.app import create_app

app = create_app(os.environ["FLASK_CONFIG"])
app.run()