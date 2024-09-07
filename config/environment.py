from pydantic import SecretStr, Field
from pydantic.v1 import BaseSettings


class Environment(BaseSettings):
    discord_token: SecretStr = Field(validation_alias="DISCORD_TOKEN")
    cleint_key: SecretStr = Field(validation_alias="CLIENT_KEY")
    client_secret: SecretStr = Field(validation_alias="CLIENT_SECRET")
    cdc_url: str = Field(validation_alias="CDC_URL")


ENVIRONMENT = Environment()
