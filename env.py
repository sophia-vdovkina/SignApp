import os
import json

APP_ENV_VAL = "development"

def set_env(variable, default):
        os.environ[variable] = os.getenv(variable, default)

class SetupAppEnvironment:

    APP_ENV_KEY = "APPLICATION_CONFIG"

    def configure_app(self):
        with open(os.path.join("config", f"{self.get_env_value()}.json")) as f:
            config = json.load(f)

        config = dict((x["name"], x["value"]) for x in config)

        for key, val in config.items():
            set_env(key, val)

    def set_app_env(self, val):
        os.environ[self.APP_ENV_KEY] = val

    def get_env_value(self):
        return os.environ[self.APP_ENV_KEY]


env = SetupAppEnvironment()
env.set_app_env(APP_ENV_VAL)