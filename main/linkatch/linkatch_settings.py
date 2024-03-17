from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LinkatchSettings(BaseSettings):
    url: str = r'https://app.linkatch.com'
    username: str = r'boaz@tensor-tech.co.il'
    password: SecretStr = None

    # Settings can be overriden using environment variables.
    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='__', env_prefix='LINKATCH')
