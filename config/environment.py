from nidavellir.environment import EnvConfig
from pydantic import SecretStr, Field
from pydantic.v1 import BaseSettings


class Environment(EnvConfig):
    discord_token: SecretStr = Field(validation_alias="DISCORD_TOKEN")


ENVIRONMENT = Environment()
