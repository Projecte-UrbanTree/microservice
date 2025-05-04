import os
from typing import Any, Union

from pydantic import MariaDBDsn, computed_field, field_validator, model_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str | None = None
    APP_PACKAGE: str = "api"
    APP_ENV: str = "development"
    IMAGE_VERSION: str | None = None

    MARIADB_SERVER: str | None = None
    MARIADB_PORT: int = 3306
    MARIADB_USER: str | None = None
    MARIADB_PASSWORD: str | None = None
    MARIADB_PASSWORD_FILE: str | None = None
    MARIADB_DB: str | None = None

    SENTRY_DSN: str | None = None

    @field_validator("IMAGE_VERSION")
    def check_image_version(cls, v):
        if v is None or v == "":
            return None
        if v.startswith("v"):
            return v[1:]
        return v

    @model_validator(mode="before")
    @classmethod
    def check_mariadb_password(cls, data: Any) -> Any:
        if data.get("APP_ENV") == "test":
            return data
        if (
            data.get("MARIADB_SERVER") is None
            or data.get("MARIADB_USER") is None
            or data.get("MARIADB_DB") is None
        ):
            raise ValueError(
                "MARIADB_SERVER, MARIADB_USER, and MARIADB_DB must be set."
            )
        if (
            data.get("MARIADB_PASSWORD_FILE") is None
            and data.get("MARIADB_PASSWORD") is None
        ):
            raise ValueError(
                "At least one of MARIADB_PASSWORD_FILE or MARIADB_PASSWORD must be set."
            )
        return data

    @field_validator("MARIADB_PASSWORD_FILE")
    def read_password_from_file(cls, v):
        if v is not None:
            file_path = v
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    return file.read().strip()
            raise ValueError(f"Password file {file_path} does not exist.")
        return v

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> Union[str, None]:
        if self.APP_ENV == "test":
            return "sqlite:///:memory:"
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            username=self.MARIADB_USER,
            password=(
                self.MARIADB_PASSWORD
                if self.MARIADB_PASSWORD
                else self.MARIADB_PASSWORD_FILE
            ),
            host=self.MARIADB_SERVER,
            port=self.MARIADB_PORT,
            path=self.MARIADB_DB,
        )


settings = Settings()
