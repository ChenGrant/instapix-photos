import os
from dotenv import load_dotenv

__ENV_FILES = {
    "dev": ".env.dev",
    "prod": ".env.prod",
}


# loads env variables based on current ENV
def load_env_var():
    file_path = os.path.dirname(os.path.abspath(__file__))
    env = os.environ.get("ENV")
    env_file = __ENV_FILES[env]
    load_dotenv(os.path.join(file_path, env_file))
    print(f"ENV = {env}")
