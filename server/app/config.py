import os
import json
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base configuration class
    """

    # Load environment variables
    URL = os.getenv("URL")

    @staticmethod
    def validate_env_vars():
        missing_vars = []

        if not Config.URL:
            missing_vars.append("URL")

        if missing_vars:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing_vars)}"
            )


def get_config():
    Config.validate_env_vars()
    return Config
