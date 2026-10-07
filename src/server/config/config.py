"""Config with pydantic settings for file-transfer"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

FILES_PATH = Path(__file__).with_name("dev.env")


class Settings(BaseSettings):
    """Loads the settings for the file transfer"""

    files_dir: Path

    model_config = SettingsConfigDict(env_file=FILES_PATH, env_file_encoding="utf-8")


settings = Settings()
