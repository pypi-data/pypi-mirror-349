from typing import Optional, Union
import ssl
from httpx import URL
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from .models import TimeoutTypes


class Infoblox(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="ib_", extra="ignore")
    host: Union[str, URL] = Field(None)
    verify_ssl: Union[bool, str, int, ssl.SSLContext] = True
    timeout: Union[TimeoutTypes] = 5.0
    username: str
    password: str
    import_timeout: int = 60
    import_retry: int = 10
    discovery_timeout: int = 60
    discovery_retry: int = 10

    @field_validator("verify_ssl")
    @classmethod
    def _verify(cls, v: Union[bool, int, str, ssl.SSLContext]) -> bool | ssl.SSLContext:
        if isinstance(v, ssl.SSLContext):
            return v
        falsy_values = {"0", "off", "false", "f", "no", ""}

        if isinstance(v, int):
            return bool(v)

        if isinstance(v, bool):
            return v

        if isinstance(v, str):
            lowered = v.strip().lower()
            if lowered in falsy_values:
                return False
            path = Path(v)
            if path.is_file():
                try:
                    context = ssl.create_default_context()
                    context.load_verify_locations(str(path))
                    return context
                except Exception as e:
                    raise ValueError(
                        f"Failed to create SSL context from path '{v}': {e}"
                    )
            return True  # All other strings treated as truthy

        raise TypeError(f"Unsupported type for verify_ssl: {type(v)}")
