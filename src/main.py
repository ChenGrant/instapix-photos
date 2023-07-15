import os
import sys
import gcp
import server

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../config")))
import config


def main():
    config.load_env_var()
    gcp.initialize()
    server.start()


if __name__ == "__main__":
    main()
